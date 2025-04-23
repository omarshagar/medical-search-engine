import os

from .profile import Profile

class CheXpert001(Profile):
    
    profile_id = 'chexpert001'
    
    def __init__(self, title: str = 'CheXpert 001', icon_name: str = 'virtual_doctor', 
                 weights_path: str = 'config/ai/weights/chexpert001.h5') -> None:
        
        super(CheXpert001, self).__init__(title=title, icon_name=icon_name, weights_path=weights_path)
        
        self._fill()
        self._complete()
        
    def _fill(self):
        
        self.metadata.add_desc(typ='inputs', block_index=0, type='image', subtype='radiograph', specialization='chest',
                               is_stream=False, min_cardinality=1, max_cardinality=2)

        self.metadata.add_desc(typ='outputs', block_index=0, type='tags', is_stream=False, min_cardinality=1, max_cardinality=14)
        
        self.metadata.add_desc(typ="preprocessing", block_index=0, read={'args_keys': ['files_urls'], 'kwargs': {}}, 
                               resize={'args_keys': ['data'], 'kwargs': {'size': [384, 384], 'interpolation': 'area'}})
        
        self.metadata.add_desc(typ='postprocessing', block_index=0)
        
    def _complete(self):
        
        self.about.greeting = f"""Hi!, I am {self.title}, actually I have a lot to do but nothing important except you."""
        self.about.info = f"""Mr. {self.title} has ability to diagnose and localize up to 14 different abnormalities."""
        self.about.specialization = f"""Chest Radiographs"""
        self.about.input_summary = """..."""
        self.about.output_summary = f"""If Mr. {self.title} suspect any abnormalities, a report is to be generated including necessary information."""
        self.about.notes = f"""Please consider that {self.title} is not experienced yet."""

    def parse(self):
        
        info = super().parse()
        info['profile_id'] = self.profile_id
        
        return info

# -----------------------------------------------------------------------------------------------------------------------------------------------------

class CheXpert002(Profile):
    
    profile_id = 'chexpert002'
    
    def __init__(self, title: str = 'CheXpert 002', icon_name: str = 'virtual_doctor', 
                 weights_path: str = 'config/ai/weights/chexpert002.h5') -> None:
        
        super(CheXpert002, self).__init__(title=title, icon_name=icon_name, weights_path=weights_path)
        
        self._fill()
        self._complete()
        
    def _fill(self):
        
        self.metadata.add_desc(typ='inputs', block_index=0, type='image', subtype='radiograph', specialization='chest',
                               is_stream=False, min_cardinality=1, max_cardinality=10)

        self.metadata.add_desc(typ='outputs', block_index=0, type='tags', is_stream=False, min_cardinality=1, max_cardinality=14)
        
        self.metadata.add_desc(typ="preprocessing", block_index=0, read={'args_keys': ['files_urls'], 'kwargs': {}}, 
                               resize={'args_keys': ['data'], 'kwargs': {'size': [384, 384], 'interpolation': 'area'}})
        
        self.metadata.add_desc(typ='postprocessing', block_index=0)
        
    def _complete(self):
        
        self.about.greeting = f"""Hi!, I am {self.title}, actually I have a lot to do but nothing important except you."""
        self.about.info = f"""Mr. {self.title} has ability to diagnose and localize up to 14 different abnormalities."""
        self.about.specialization = f"""Chest Radiographs"""
        self.about.input_summary = """..."""
        self.about.output_summary = f"""If Mr. {self.title} suspect any abnormalities, a report is to be generated including necessary information."""
        self.about.notes = f"""Please consider that {self.title} is not experienced yet."""

    def parse(self):
        
        info = super().parse()
        info['profile_id'] = self.profile_id
        
        return info