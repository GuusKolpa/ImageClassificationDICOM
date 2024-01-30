import logging

import SimpleITK
from pydicom import dcmread

class DicomData:
    """ Class that converts DICOMs to NIFTI images and corresponding JSON files containing the headers. """
    logging.debug()