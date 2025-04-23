from .profile import Profile

class Mura(Profile):
    
    profile_id = 'mura001'
    
    def __init__(self) -> None:
        
        super().__init__()
        
        self.title = "Mura 001"
        
        self._fill()
        self._complete()
        
    def _fill(self):
                
        self.metadata.add_desc(typ='inputs', block_index=0, type='image', subtype='radiograph', specialization='chest', 
                               is_stream=False, min_cardinality=1, max_cardinality=2)

        self.metadata.add_desc(typ='outputs', block_index=0, type='tags', is_stream=False, min_cardinality=1,
                               max_cardinality=14, threshold=0.5, values_range=(0, 14))

        self.metadata.add_desc(typ="preprocessing", block_index=0, read={'args_keys': ['files_urls'], 'kwargs': {}}, 
                               resize={'args_keys': ['data'], 'kwargs': {'size': [256, 256], 'interpolation': 'area'}})
        
        self.metadata.add_desc(typ='postprocessing', block_index=0)
        
    def _complete(self):
        
        self.about.greeting = """Hi!, I am Mura-001, actually I have a lot to do but nothing important except you."""
        self.about.info = """Mr. Mura-001 has ability to diagnose and localize up to 14 different abnormalities."""
        self.about.specialization = """Chest Radiographs"""
        self.about.input_summary = """..."""
        self.about.output_summary = """If Mr. Mura-001 suspect any abnormalities, a report is to be generated including necessary information."""
        self.about.notes = """Please consider that Mura-001 has no too much experience yet."""

    def parse(self):
        
        info = super().parse()
        info['profile_id'] = Mura.profile_id
        
        return info
