from ImageClassifier.ioutils.dicom import DicomData

SERIES_DESCRIPTION_LUT = {
    't2': ["AX OB T2WTSE", "AX OBL T2 BLADE SMFOV", "AX T2", "AX T2 FSE 3mm", "AX T2 NO ANGLE", "AX T2 PROPELLER",
                 "AX T2 SM FOV",  "AX T2 TSE", "AX T2tseSMFOV", "AXT2", "Ax Cube T2-100ETL2Rx", "Ax T2",
                 "Ax T2 FRFSE PROP", "Ax T2 PROPELLER", "Axial T2", "SCAx T2 FSE", "T2 AX", "T2 AX TSE SMALL FOV",
                 "T2 Ax", "T2 Ax SPACE Prostate PlaneTop of Bladder-Thru Prostate", "T2WTSE AX HI",
                 "reprat t2spcrstaxial oblProstate", "t2spcrstax oblp2", "t2spcrstaxial Prostate",
                 "t2spcrstaxial oblProstate", "t2spcrstaxial oblProstate rpt", "t2spcrstaxial oblRPT",
                 "t2spcrstaxial oblp2", "t2spcrstaxialProstate", "t2spcrstaxialProstate rpt", "t2spcrstaxialp2",
                 "t2spcrstaxp2", "t2spctrap2rstaxial oblProstate", "t2spctrap2rstaxialProstate", "t2tsetra",
                 "t2tsetra obl 3mm", "t2tsetra320p2", "t2tsetraprostate", "t2tsecor", "AX T2 FSE", "Ax T2 HR  FRFSE",
                "T2 SPACE 3D AXIAL", "AX FSE T2 SMALL"],
    'adc': ["diffusiontrab10001500ADC", "ep2d-advdiff-3Scan-4bvalspairUpper ProstateADC",
            "ep2d-advdiff-3Scan-4bvalspairstdADCDFCMIX", "ep2ddiffb01004008001400ADC", "AX DWINBHADC",
            "AX DIFF EP2DADC", "dSShDWI ADC COMBO", "ep2ddiffb0100400800ADCDFC", "Ax Diff B 507501000ADC",
            "ep2ddiffb0100400800ADCDFCMIX", "ep2d-advdiff-3Scan-4bvalspair Upper ProstateADCDFCMIX",
            "Apparent Diffusion Coefficient mm2s", "AX DWI FS ZOOM 1006001000ADCDFCMIX", "DWI AXADCDFCMIX",
            "ep2d-advdiff-3Scan-4bvalspairstdADC", "ADC", "ADC 10-6 mms", "ep2ddiffb 0100400800ADC",
            "ep2ddiffb0100400800ADC", "AX DWI B50 B400 B800ADC", "DIFFUSION B1000 1500ADC", "eDWI 3 bADC",
            "resolvediffb1008001400 AXp2ADC", "AX DIFF NO ANGLE B0504001400ADC", "ep2ddiff b50b1000b1600b2000 smallADC",
            "ep2d-advdiff-3Scan-4bvalspairstd RepeatADCDFCMIX", "DIFFUSION AXADC",
            "rFOV Apparent Diffusion Coefficient Map", "ep2ddiffb50100016002000 trap2ADCDFCMIX",
            "ep2d-advdiff-3Scan-4bvalspair Upper ProstateADC", "ep2d-advdiff-3Scan-4bvalspairstd APADC",
            "ep2ddiffb4008001000ADC", "ep2ddiff b50b1000b1600b2000 smaller fovADCDFCMIX",
            "ep2d-advdiff-3Scan-4bvalspairstdADCDFC", "ep2d-advdiff-3Scan-4bvalspairstdupperADC",
            "ep2d-advdiff-3Scan-4bvalspair Upper ProstateADCDFC", "DIFF Ax 2ADC", "dDWI ADC", "DWIADCDFC", "dADC 100"],
    'bvalue_high': ["Ax eDWI CALCBVAL", "ep2d-advdiff-3Scan-4bvalspairstdCALCBVAL",
                    "ep2d-advdiff-3Scan-4bvalspairstdupperCALCBVAL", "ep2d-advdiff-3Scan-4bvalspairCALCBVAL",
                    "ep2ddiffb0100400800CALCBVALDFCMIX", "ep2d-advdiff-3Scan-4bvalspair Upper ProstateCALCBVAL",
                    "ep2d-advdiff-3Scan-4bvalspair Upper ProstateCALCBVALDFC",
                    "ep2d-advdiff-3Scan-4bvalspairstdCALCBVALDFC",
                    "ep2d-advdiff-3Scan-4bvalspairUpper ProstateCALCBVAL",
                    "ep2d-advdiff-3Scan-4bvalspairstdCALCBVALDFCMIX",
                    "ep2d-advdiff-3Scan-4bvalspairstd RLCALCBVAL", "AX DWI FS ZOOM 1006001000CALCBVAL",
                    "ep2ddiffb0100400800CALCBVAL", "ep2d-advdiff-3Scan-4bvalspair Upper ProstateCALCBVALDFCMIX",
                    "B1500T", "CALCBVAL", "ep2ddiffb01004008001400CALCBVAL", "ep2ddiff b50b1000b1600b2000CALCBVAL",
                    "resolvediffb1008001400 AXp2CALCBVAL", "ep2d-advdiff-3Scan-b value 1400",
                    "B1600 AX", "AX DWI B50 B400 BCALCBVAL", "ep2d-advdiff-3Scan-1400bvalspair",
                    "ep2ddiffb0100400800CALCBVALDFC", "ep2ddiffb1400", "DWICALCBVALDFC", "DWI AXTRACEWDFCCALCBVAL",
                    "DWI 504001400", "Ax DWIAll b-50 1000 1500 2000", "DIFF B1600", "B1000",
                    "Reg - Reg - DWIB01008001400", "Ax DWI B1500", "ep2d-advdiff-1400bvalspairstd", "AX DIFF EP2D",
                    "Ax DWI b1400", "Ax DWI ORIGINAL", "AX DIFF NO ANGLE B0504001400", "Ax DWI 1400", "Ax DWIAll b1400",
                    "ep2d-advdiff-3Scan-1400 bvalspairstdTRACEW", "SShDWI", "eDWI 3 b-value 504001400", "Ax DWI",
                    "Ax DWI rFOV b1350", "B1600", "sDWI B2000 PACS ONLY", "Ax FOCUS 50 800 1500", "AX DWINBH",
                    "ep2ddiffb1400TRACEW"]
}


def dataset_preprocessing_function(dicom_object: DicomData) -> DicomData:
    """ For PMUB cases, all underscores ('_') are removed from the DICOM tag 'SeriesDescription' (0008,103e). """
    series_description = dicom_object.get_dicom_tag('0008103E')
    dicom_object.set_dicom_tag('0008103E', series_description.replace('_', ''))
    return dicom_object
