from typing import List

import numpy as np
import cv2 as cv


def normalize_in_range(a: np.ndarray, min_value: float, max_value: float, axes: List[str]):
    
    b = (a - a.min(axis=tuple(axes), keepdims=True)) / a.max(axis=tuple(axes), keepdims=True)
    c = max_value * b + min_value
    
    return c


def is_gray(image: np.ndarray):
    
    return (image.ndim == 2) or (image.shape[-1] == 1)

