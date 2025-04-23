from typing import Dict

from ..config import Config

from .handlers.base import Handler, Collections

from .handlers.chexpert001 import CheXpert001
from .handlers.chexpert002 import CheXpert002

from ..wrappers import types

def get(model_id) -> Handler:
    
    return Collections.get(model_id=model_id)(model_metadata=Config.models[model_id])

def get_all() -> Dict[str, Handler]:
    
    models = {}
    
    for _id in Collections._all:
        
        models[_id] = get(_id)
    
    return types.ReadOnlyDict(models)

