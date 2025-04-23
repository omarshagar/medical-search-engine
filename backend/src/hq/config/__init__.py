import json
import pathlib

from ..wrappers import types

from . import virtual_doctors_profiles
from .virtual_doctors_profiles.profile import Metadata


CONFIG_PATH_LIST = {
    'specialized_quest_types': 'specialized_quest_types.json',
    'commands': 'queries/commands.json',
    'models': 'ai/models.json',
    'files': 'files.json'
}

def get_path(name: str, depth: int = 0):

    working_directory = pathlib.Path(__file__).parent

    for _ in range(depth):

        working_directory = working_directory.parent

    path = CONFIG_PATH_LIST[name]
    path = working_directory.joinpath(path)
    
    return path


def get(name: str, depth: int = 0):

    path = get_path(name, depth=depth)
    
    with open(path, 'r') as read_buffer:

        cfgs = json.load(read_buffer)

    return types.ReadOnlyDict(cfgs)


class Config:

    virtual_doctors_profiles.to_json(path=get_path('models'))
    
    specialized_quest_types = get('specialized_quest_types')
    commands = get('commands')
    models = get('models')
    files = get('files')
