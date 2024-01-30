import argparse
import logging
from pathlib import Path

from ImageClassifier.logger.setup_logger import setup_logging
from ImageClassifier.ioutils.dicom import DicomData

logger = logging.getLogger(__name__)


def generate_niftis(directory: Path):
    dicom_object = DicomData.from_dicom_dir(directory)
    print(dicom_object.get_dicom_tag('0008103E'))


def get_parser():
    parser = argparse.ArgumentParser(description='Generates NIFTI files for dataset from a given input directory '
                                                 'containing DICOM series.')

    parser.add_argument('--input_directory', help='Path to the input directory containing DICOM images.',
                        type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()

    p = get_parser()
    generate_niftis(p.input_directory)
