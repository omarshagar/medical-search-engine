import os.path
from typing import Union, List, Set

from pathlib import Path


def is_file(path: str) -> bool:

    return Path(path).is_file()


def is_directory(path: str) -> bool:

    return Path(path).is_dir()


def check_supported_extensions(path: str, supported_extensions: Union[List[Set[str]], Set[str]]):

    extension = os.path.splitext(path)[-1]

    if isinstance(supported_extensions, list):

        for extensions in supported_extensions:

            if extension in extensions:

                return True

        return False

    else:

        return extension in supported_extensions
