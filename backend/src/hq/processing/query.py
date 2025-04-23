from typing import Dict, Any, List
from . import image
from ..config import Config

def preprocess_ongoing_query(ongoing_query: Dict[Any,Any]):
    
    metadata = ongoing_query['metadata']
        
    for i in range(len(metadata)):
    
        preprocess = get_preprocessing_steps_per_block(metadata[i])
        
        for fn_name in preprocess:
            
            if fn_name not in image.PROCESSORS:
            
                continue
            
            assert ('args_keys' in preprocess[fn_name]) and ('kwargs' in preprocess[fn_name]), 'Invalid preprocessing method definition'
            
            args_keys = preprocess[fn_name]['args_keys']

            if len(args_keys) == 1:
                
                arg_key = args_keys[0]
                args_list = [(arg, ) for arg in ongoing_query[arg_key]]
                
            else:
                   
                args_list = zip([ongoing_query[key] for key in args_keys])
            
            kwargs = preprocess[fn_name]['kwargs']
                            
            for idx, args in enumerate(args_list):

                output = image.PROCESSORS[fn_name](*args, **kwargs)

                if idx < len(ongoing_query['data']):
                    
                    ongoing_query['data'][idx] = output
                
                else:
                    
                    ongoing_query['data'].append(output)


    assert len(ongoing_query['data']) > 0, 'preprocess_ongoing_query(...) failed, e.g., did not found any preprocessing function to execute'

def get_preprocessing_steps_per_block(file_metadata: Any):
    
    model_id = file_metadata['model']
    block_index = file_metadata['block_index']

    model_metadata = Config.models[model_id]['metadata']
    preprocessing_metadata = model_metadata['preprocessing']
    
    return preprocessing_metadata[block_index]

