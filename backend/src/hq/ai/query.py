from typing import Dict, Any, List

from . import get_all

MODELS = get_all()

def predict_per_spectialization(query_id: str, model_id: str, query_inputs: List[Any]):
        
    inputs = {}
    
    for block in query_inputs:
        
        block_index = str(block['block_index'])
        
        if block_index not in inputs:
            
            inputs[block_index] = []
        
        inputs[block_index].append(block['data'])
    
    MODELS[model_id].run(buffer_index=query_id, inputs=inputs)


def predict(gathered_query: Dict[Any, Any]):
    
    finshed_query = gathered_query
    
    query_id = gathered_query['query_id']
    
    for spec in gathered_query['content']:
        
        model_id = gathered_query['content'][spec]['model_id']
        inputs = gathered_query['content'][spec]['inputs']
        
        predict_per_spectialization(query_id=query_id, model_id=model_id, query_inputs=inputs)

        finshed_query['content'][spec]['outputs'] = MODELS[model_id].finalize(buffer_index=query_id)
        
    return finshed_query
