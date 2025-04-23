import os

from typing import Dict, Set, Any

from ... import utils

class Collections:
    
    _all = {}
    
    def register(cls):
        
        Collections._all[cls.model_id] = cls

    def get(model_id):
        
        return Collections._all[model_id]

class Handler:
    
    def __init__(self, model_metadata: Dict[Any, Any]):

        self.model_metadata = model_metadata

        self.inputs_buffer = {}
        self.metadata_buffer = {}
        self.intermediate_buffer = {}
        self.outputs_buffer = {}
        
        # inputs descriptors
        self.inputs_desc: Set[Any] = None
        
        # outputs descriptors
        self.outputs_desc: Set[Any] = None
        
        self.working_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '/../..'
        
        self.build()

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        
        Collections.register(cls)
        
    @property
    def id(self):
        
        raise NotImplementedError('...')
    
    def build(self):
        
        raise NotImplementedError('...')
    
    # define inputs descriptors
    def set_inputs_desc(self, keys: Any, dtypes: Any):
        
        self.inputs_desc = set(zip(keys, dtypes))
    
    # define outputs descriptors
    def set_outputs_desc(self, keys: Any, dtypes: Any):
        
        self.outputs_desc = set(zip(keys, dtypes))
    
    # get inputs descriptors
    def _get_inputs_desc(self, inputs):
        
        desc = set([(key, type(value)) for key, value in inputs.items()])

        return desc

    # get outputs descriptors
    def _get_outputs_desc(self, outputs):
        
        desc = set([(key, type(value)) for key, value in outputs.items()])

        return desc
    
    # match inputs/outputs descriptors
    def _assert_invalid_desc(self, desc1: Set[Any], desc2: Set[Any], signature: str):
        
        for (key1, dtype1), (key2, dtype2) in zip(desc1, desc2):

            assert (key1 == key2) and (dtype1 == dtype2), f'Inconsistent {signature} descriptors' 
    
    
    # inputs in a (key, value) format, where key must be "block_index"    
    def apppend_inputs(self, buffer_index: str, inputs: Dict[str, Any]):
        
        """
            append inputs to its associated buffer
        """     
        self._assert_invalid_desc(self._get_inputs_desc(inputs), self.inputs_desc, signature='inputs')

        self.inputs_buffer[buffer_index] = inputs
    
    # outputs in a (key, value) format, where key must be "block_index"
    def append_outputs(self, buffer_index: str, outputs: Dict[str, Any]):
        
        """
            append outputs to its associated buffer
        """     
        
        self._assert_invalid_desc(self._get_outputs_desc(outputs), self.outputs_desc, signature='outputs')
        
        self.outputs_buffer[buffer_index] = outputs     

    def prepare(self):

        """
            1) Prepare inputs (e.g., may convert rgb image to grayscale, text to a model specific tokens, etc.)
            2) Set results to intermediate which being used for inference step
        """
        
        raise NotImplementedError('...')

    def run_inference(self, layer_name=None):

        raise NotImplementedError('...')

    def run_postprocessing(self):

        raise NotImplementedError('...')
    
    def finalize(self, buffer_index: str):
        
        del self.inputs_buffer[buffer_index]
        del self.intermediate_buffer[buffer_index]
        
        if buffer_index in self.metadata_buffer:
            
            del self.metadata_buffer[buffer_index]
            
        return self.outputs_buffer.pop(buffer_index)

    def run(self, buffer_index: str, inputs: Dict[str, Any]):
        
        self.apppend_inputs(buffer_index=buffer_index, inputs=inputs)
        self.prepare()
        self.run_inference()
        self.run_postprocessing()
        
    def reset(self):

        self.inputs_buffer = {}
        self.metadata_buffer = {}
        self.intermediate_buffer = {}
        self.outputs_buffer = {}

    @property
    def buffer_size(self):

        return max(len(self.inputs_buffer), len(self.metadata_buffer),
                   len(self.intermediate_buffer), len(self.outputs_buffer))
    