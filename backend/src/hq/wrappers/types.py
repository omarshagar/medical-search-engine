from typing import Dict, Any

import copy


class ReadOnlyDict(dict):

    def __init__(self, data, **kwargs):

        super().__init__(data, **kwargs)

    def __setitem__(self, key, value):

        raise NotImplementedError('Invalid attempt to modify read-only dictionary, __setitem__(...) does not exist')

    def __delitem__(self, key):

        raise NotImplementedError('Invalid attempt to modify read-only dictionary, __delitem__(...) does not exist')

    def pop(self, key):

        raise NotImplementedError('Invalid attempt to modify read-only dictionary, pop(...) does not exist')

    def update(self, __m, **kwargs):

        raise NotImplementedError('Invalid attempt to modify read-only dictionary, update(...) does not exist')
    
    def copy(self) -> Dict[Any, Any]:
        
        return copy.deepcopy(super().copy())