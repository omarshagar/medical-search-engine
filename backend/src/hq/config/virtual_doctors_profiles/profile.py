from abc import ABC

from ...wrappers.types import ReadOnlyDict

class Collections:
    
    _all = {}
    
    def register(cls):
        
        Collections._all[cls.profile_id] = cls

    def get(profile_id):
        
        return Collections._all[profile_id]

class Metadata:
    
    # ordered
    tag_keys = ['type', 'subtype', 'specialization']

    def __init__(self):
        
        self._inputs = []
        self._outputs = []
        self._preprocessing = []
        self._postprocessing = []

    def add_desc(self, typ, **kwargs):
        
        getattr(self, '_' + typ).append(kwargs)
    
    @property
    def inputs(self):
        
        return self._inputs
    
    @property
    def outputs(self):
        
        return self._outputs

    @property
    def preprocessing(self):

        return self._preprocessing
        
    @property
    def postprocessing(self):

        return self._postprocessing

    @staticmethod
    def get_tags(input_metadata):
        
        tags = []
        
        for key in Metadata.tag_keys:
                        
            tags.append(input_metadata[key])
            
        return tags
    
    def to_dict(self):
        
        return ReadOnlyDict(self.__dict__)
    
class About:
    
    def __init__(self):
        
        self.greeting: str = None
        self.info: str = None
        self.specialization: str = None
        self.input_summary: str = None
        self.output_summary: str = None
        self.notes: str = None
    
    def to_dict(self):
        
        return ReadOnlyDict(self.__dict__)
    
class Profile(ABC):
    
    def __init__(self, title: str = None, icon_name: str = 'virtual_doctor', weights_path: str = None) -> None:
        
        self.title: str = title
        self.icon_name: str = icon_name 

        self.weights_path: str = weights_path
        
        self.about = About()
        self.metadata = Metadata()
        
    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        
        Collections.register(cls)
        
    def _fill(self):
        
        raise NotImplementedError('...')
    
    def _complete(self):
        
        raise NotImplementedError('...')

    def parse(self):
        
        data = self.__dict__
        
        def _parse(_data):
            
            for key, value in _data.items():
                
                if not hasattr(value, 'to_dict'):
                    
                    continue
                
                else:
                    
                    value_next = value.to_dict()
                    
                    if not hasattr(value_next, 'to_dict'):
                        
                        _data[key] = {}
                        
                        for ckey, cvalue in value_next.items():

                            if ckey.startswith('_'):
                                
                                ckey = ckey[1:]
                            
                            _data[key][ckey] = cvalue

                    else:
                        
                        if key.startswith('_'):
                                
                            key = key[1:]
                        
                        _data[key] = value_next
                        
                        _parse(_data[key])
        
        _parse(data)

        return data
