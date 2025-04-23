from . import common, memory
from .memory import Unit

from ...config import Config

CHECKERS = {}

def register_verify_method(typ):
    
    def register(fn):
        
        CHECKERS[typ] = fn
    
    return register

@register_verify_method(typ='image')
def verify_image(path: str) -> None:

    files_config = Config.files['image']

    if not common.is_file(path):

        raise ValueError(f'Invalid path for an image')

    supported_extensions = files_config['supported_extensions']

    
    common.check_supported_extensions(path, supported_extensions)

    max_size = files_config['max_size']

    unit = Unit.get(max_size['unit'])
    size = memory.file_size(path, unit)

    if size > max_size['value']:

        return path
    
    # valid case
    return None
