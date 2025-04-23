from typing import Dict, Union, Any

import os
import numpy as np

import cv2 as cv
import pydicom as dicom

 # ---------------------------------------------------------------------------------------------------------------------------------------------------

READERS = {}
WRITERS = {}

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def register_readers(extensions):
    
    def register(fn):
        
        for ext in extensions:
            
            READERS[ext] = fn
            
    return register


# ---------------------------------------------------------------------------------------------------------------------------------------------------

def register_writers(extensions):
    
    def register(fn):
        
        for ext in extensions:
            
            WRITERS[ext] = fn
            
    return register
            
# ---------------------------------------------------------------------------------------------------------------------------------------------------

@register_readers(extensions=['jpg', 'png', 'jpeg'])
def read_cv(path: str) -> np.ndarray:

    """ Read an image of the following extensions: {jpg, PNG, jpeg, tiff, jfif}

        Args:
            path (str): path of image data to be loaded
            mode (int): flag that can take values of cv::ImreadModes
        Return:
            np.ndarray: array of pixels, dtype=np.float32
    """

    image = cv.imread(path, cv.IMREAD_UNCHANGED)

    return image


# ---------------------------------------------------------------------------------------------------------------------------------------------------


@register_readers(extensions=['dcm', 'img'])
def read_dicom(path: str, bytes_limit: Union[int, float, str] = None,
               metadata_only: bool = False, parse_metadata: bool = False,
               pixel_dtype: np.dtype = None, **kwargs) -> Dict[Any, Any]:

    """ Read an image of the following extensions: {jpg, PNG, jpeg, tiff, jfif}

        Args:
            path (str): path of image data to be loaded

            bytes_limit (Union[int, float, str]):  if a data element's stored value is larger than bytes_limit,
                                       value is not read into memory until it is accessed in code, default=None

            metadata_only (bool): if False then pixels-data will not be read, default=False
            parse_metadata (bool): if False, then only pixels-data will be returned, default=False
            pixel_dtype (np.dtype): pixels data type, default=None
        Return:
            np.ndarray: array of pixels, dtype=np.float32
    """

    assert not parse_metadata or not metadata_only, 'Parse metadata is not yet supported'

    dicom_dataset = dicom.dcmread(path, defer_size=bytes_limit, stop_before_pixels=metadata_only, **kwargs)

    pixel_data = dicom_dataset.pixel_array

    if pixel_dtype is not None:

        pixel_data = np.asarray(pixel_data, dtype=pixel_dtype)

    data = {'pixel_data': pixel_data}

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------

@register_writers(extensions=['jpg', 'png', 'jpeg'])
def write_cv(image, path: str):

    """ Write an image in the following extensions: {jpg, PNG, jpeg, tiff, jfif} """

    cv.imwrite(path, image)

# ----------------------------------------------------------------------------------------------------------------------------------------------------


def get_extension(path: str):
    return os.path.splitext(path)[-1][1:]


# ----------------------------------------------------------------------------------------------------------------------------------------------------

