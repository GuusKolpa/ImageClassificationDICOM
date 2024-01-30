import json
import logging
from pathlib import Path
from typing import Union, Callable, Any

import SimpleITK as sitk
from pydicom import dcmread

logger = logging.getLogger(__name__)


class DicomData:
    """ Class that converts DICOMs to NIFTI images and corresponding JSON files containing the headers. """

    def __init__(self, pixel_data: sitk.Image, dicom_headers: dict, dicom_name: str):
        self.pixel_data = pixel_data
        self.dicom_headers = dicom_headers
        self.dicom_name = dicom_name

    @classmethod
    def from_dicom_dir(cls, dicom_dir: Path):
        """ Initializes a DicomData object from a given valid DICOM directory.

        Args:
            dicom_dir: Directory containing a single DICOM series.
        """

        dicom_reader = sitk.ImageSeriesReader()
        header_reader = sitk.ImageFileReader()
        try:
            logger.info(f"Reading DICOMs from {dicom_dir}")
            series = dicom_reader.GetGDCMSeriesIDs(str(dicom_dir))
            dcm_ordering_list = []
            if len(series) > 1:
                raise ValueError(f"DICOM contains multiple SeriesInstanceUIDs in directory: {dicom_dir}")
            for series_id in series:
                for filename in dicom_reader.GetGDCMSeriesFileNames(str(dicom_dir), series_id):
                    header_reader.SetFileName(filename)
                    header_reader.ReadImageInformation()
                    instance_number = _tag_from_image_file_reader(header_reader, '0020|0013', int)
                    dcm_ordering_list.append({'filename': filename, 'instancenumber': instance_number})
        except Exception as e:
            logger.error(f"Could not load DICOM series: {e}")

        # Order the DICOM list by InstanceNumber.
        ordered_dicom_list = sorted(dcm_ordering_list, key=lambda x: x['instancenumber'])
        logger.debug(f"Ordered DICOM list of length {len(ordered_dicom_list)}")
        dicom_reader.SetFileNames([fname['filename'] for fname in ordered_dicom_list])
        image = dicom_reader.Execute()

        # Read DICOM headers from the first file in the series.
        first_dicom = ordered_dicom_list[0]['filename']
        dicom_header = dcmread(first_dicom, stop_before_pixels=True)

        # Valid tags are surpressed when converting DICOM headers to dictionary.
        dicom_header_dict = json.loads(dicom_header.to_json(suppress_invalid_tags=True))
        logger.debug(f"Succesfully loaded image and DICOM headers from {dicom_dir}")

        return cls(image, dicom_header_dict, Path(first_dicom).name)

    def save_to_json_and_nifti(self, output_directory: Path, filename: str):
        """ Saves the loaded image and DICOM dictionary as a NIFTI (.nii.gz) and JSON (.json) file.

        Args:
            output_directory: The directory in which to save the resulting files.
            filename: The filename for the T2 and JSON files.
        """
        if not output_directory.is_dir():
            output_directory.mkdir(parents=True)

        nifti_out_file = output_directory / f'{filename}.nii.gz'
        json_out_file = output_directory / f'{filename}.json'
        logger.debug(f"Writing out image data to {nifti_out_file}...")
        sitk.WriteImage(self.pixel_data, str(nifti_out_file))

        with json_out_file.open('w') as f:
            logger.debug(f"Writing out JSON data to {json_out_file}...")
            json.dump(self.dicom_headers, f, indent=4)

    def get_dicom_tag(self, tag: str) -> Any:
        """ Gets a DICOM tag from the DicomData object by reading the header dictionary. If resulting value is a
        list of length 1, returns the value. If a tag does not exist, return None. """
        if tag in self.dicom_headers:
            value = self.dicom_headers.get(tag)['Value']
            if isinstance(value, list) and (len(value) == 1):
                return value[0]
            else:
                return value
        else:
            logger.debug(f"DICOM tag '{tag}' does not exist in DICOM header")

    def set_dicom_tag(self, tag: str, value: Any):
        """ Sets the specific DICOM tag to a provided value. The value can be anything and does not need to adhere to
        DICOM standards. """
        self.dicom_headers[tag]['Value'] = value


def _tag_from_image_file_reader(metadata_reader: sitk.ImageFileReader, tag: str,
                                return_type: Callable = None) -> Union[None, str]:
    if metadata_reader.HasMetaDataKey(tag):
        if return_type:
            return return_type(metadata_reader.GetMetaData(tag))
        else:
            return metadata_reader.GetMetaData(tag)
