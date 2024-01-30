import argparse
import importlib
import logging
from pathlib import Path
from typing import List

from ImageClassifier.logger.setup_logger import setup_logging
from ImageClassifier.ioutils.dicom import DicomData

logger = logging.getLogger(__name__)


def load_dataset_specific_config(dataset_name: str):
    return importlib.import_module(f'ImageClassifier.resources.{dataset_name}')


def _list_all_series(input_dir: Path) -> List[Path]:
    series_path_list = []
    for patient_dir in input_dir.iterdir():
        if not patient_dir.is_dir():
            continue
        for study_dir in patient_dir.iterdir():
            if not study_dir.is_dir():
                continue
            for series_dir in study_dir.iterdir():
                if not series_dir.is_dir():
                    continue
                series_path_list.append(series_dir)
    return series_path_list


def _classify_series(series_description: str) -> str:
    for simplified_series, series_lut in SERIES_DESCRIPTION_LUT.items():
        if series_description in series_lut:
            return simplified_series
    return 'Other'


def generate_niftis(input_dir: Path, output_dir: Path): 
    """Generates NIFTI files for dataset from a given input directory containing DICOM series. Expects a top level
    directory with ./PATIENT/STUDY/SERIES/*.dcm subdirectory structure.
    
    Args:
        input_dir: 
        output_dir: 

    Returns:

    """
    logger.info(f"Generating NIFTIs for directory: {input_dir}")
    series_directory_list = _list_all_series(input_dir)
    total_number_series = len(series_directory_list)

    # Loop over all series within the subdirectories.
    for idx, series_dir in enumerate(series_directory_list):
        logger.debug(f"Processing series directory {series_dir} ({idx} / {total_number_series})")
        dicom_object = DicomData.from_dicom_dir(series_dir)
        processed_image = dataset_preprocessing_function(dicom_object)
        simplified_series = _classify_series(processed_image.get_dicom_tag('0008103E'))
        patient_id, studydate = processed_image.get_dicom_tag('00100020'), processed_image.get_dicom_tag('00080020')

        if patient_id is None or studydate is None:
            raise ValueError(f"PatientID or StudyDate can not be empty. Please fix the input images.")

        image_output_path = output_dir / patient_id / studydate / simplified_series
        dicom_object.save_to_json_and_nifti(image_output_path, simplified_series)

    # Loop over each DICOM subdirectory
    # dicom_object = DicomData.from_dicom_dir(input_dir)
    # Classify DICOM series - PATIENTID, StudyDate, SeriesClass
    # dicom_object.save_to_json_and_nifti(output_dir, 't2')


def get_parser():
    parser = argparse.ArgumentParser(description="Generates NIFTI files for dataset from a given input directory "
                                                 "containing DICOM series. Expects a top level directory with "
                                                 "./PATIENT/STUDY/SERIES/*.dcm subdirectory structure.")

    parser.add_argument("--input_directory", help="Path to the input directory containing DICOM images.",
                        type=Path, required=True)
    parser.add_argument("--output_directory", help="Path to the top-level output directory in which to save NIFTI and "
                                                   "JSON files.",
                        type=Path, required=True)
    parser.add_argument("--dataset_name", help="Provide the dataset name to load its config and Series LUT. Must "
                                               "correspond with a library in the 'resources' package.",
                        type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()

    p = get_parser()
    resource_module = load_dataset_specific_config(p.dataset_name)
    SERIES_DESCRIPTION_LUT = getattr(resource_module, 'SERIES_DESCRIPTION_LUT')
    dataset_preprocessing_function = getattr(resource_module, 'dataset_preprocessing_function')
    generate_niftis(p.input_directory, p.output_directory)
