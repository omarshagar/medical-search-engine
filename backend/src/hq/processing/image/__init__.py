from typing import Any

import cv2 as cv

from . import io, asserts, constants

# ---------------------------------------------------------------------------------------------------------------------------------------------------

PROCESSORS = {}

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def register(fn):
    
    PROCESSORS[fn.__name__] = fn

# ---------------------------------------------------------------------------------------------------------------------------------------------------

@register
def resize(image: Any, size: Any, interpolation: str = 'area', **kwargs) -> Any:

    if interpolation not in constants.Resize.methods:
        
        asserts.assert_unsupported_method(signature='resize')

    method = constants.Resize.methods[interpolation]
    
    image = cv.resize(image, dsize=tuple(size), interpolation=method, **kwargs)
        
    return image

# ---------------------------------------------------------------------------------------------------------------------------------------------------

@register
def read(path: str, **kwargs):
    
    extension = io.get_extension(path)

    if extension not in io.READERS:
        
        asserts.assert_unsupported_extensions_raise(signature='read')
    
    return io.READERS[extension](path, **kwargs)
        
 
 # ---------------------------------------------------------------------------------------------------------------------------------------------------

@register
def write(image: Any, path: str, **kwargs):
    
    extension = io.get_extension(path)

    if extension not in io.WRITERS:
        
        asserts.assert_unsupported_extensions_raise(signature='write')
    
    return io.WRITERS[extension](image, path, **kwargs)

# ---------------------------------------------------------------------------------------------------------------------------------------------------

        

