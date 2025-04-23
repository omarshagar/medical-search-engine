from typing import Dict, Any, List

from ..utils import graph

from ..config import Config
from .checkers import preload

CHECKERS = {}


def ready_check_per_block(url_list: List[str], model_id: str, block_index: int):
    
    metadata = Config.models[model_id]['metadata']
    
    assert len(metadata['inputs']) > block_index, 'block_inex out of range'
    
    block_metadata = metadata['inputs'][block_index]

    is_valid = True
    
    for key, checker_args in block_metadata.items():
        
        if key in CHECKERS:
            
            is_valid &= CHECKERS[key](url_list, checker_args)
    
    return is_valid


def ready_check(pure_query: Dict[Any, Any]):

    content = pure_query['content']
    
    model_id = content['model_id']
    
    is_valid = True
    failures = []
    
    def is_not_block_index(key):
        
        return (not isinstance(key, int))
    
    parent_graph = {}
        
    for node, parent in graph.make_dfs_iterator(content, has_cycle=False, return_parent=True, start_node='types', condition=is_not_block_index):
        
        if parent is not None:
            
            parent_graph[node] = parent
        
        # If child indicates block_index
        if isinstance(node, int):
            
            is_valid &= ready_check_per_block(url_list=content[node], model_id=model_id, block_index=node)

            content_type = node
            
            while parent_graph[content_type] != 'types':
                
                content_type = parent_graph[content_type]

            for url in list(content[node]):

                ret = preload.CHECKERS[content_type](url)

                if ret is not None:

                    content[node].remove(url)
                    failures.append(ret)

            is_valid &= ready_check_per_block(url_list=content[node], model_id=model_id, block_index=node)

    if not is_valid:
        
        return failures
    
    # valid    
    return None
