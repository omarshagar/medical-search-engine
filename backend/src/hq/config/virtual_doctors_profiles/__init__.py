from typing import Dict, Set

import json

from .. import types

from .profile import Profile, Collections
from .chexpert import *
from .mura import *

def get(profile_id) -> Profile:
    
    return Collections.get(profile_id=profile_id)()

def profiles_id() -> Set:

    return Collections._all.keys()

def get_all() -> Dict[str, Profile]:
    
    profiles = {}
    
    for _id in profiles_id():
        
        profiles[_id] = get(_id)
    
    return types.ReadOnlyDict(profiles)


def to_json(path: str):
    
    profiles = {}
    
    for _id in profiles_id():
        
        profiles[_id] = get(_id).parse()
    
    with open(path, 'w') as write_buffer:
        
        json.dump(profiles, write_buffer)
