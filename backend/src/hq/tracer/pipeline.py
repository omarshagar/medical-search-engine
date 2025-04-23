import copy
import time

from typing import List, Dict, Any
from ..processing import query as query_preprocess
from .. import processing
from ..verification import query as query_validation
from ..ai import query as query_predict
from ..controller.query import parse  as query_parser

from concurrent.futures import ThreadPoolExecutor
        
# ----------------------------------------------------------------------------------------------------------------------------------------

class Command:
        
    main_path = {'predict': []}
    
    def register(fn, key, index):
        
        Command.main_path[key].insert(index, fn)

# ----------------------------------------------------------------------------------------------------------------------------------------

class QueryStates:
    
    _id = -1
    
    _memory = {'active_gathered': {}, 
               'ready_gathered': {}, 
               'finalized': {}}
    
    @staticmethod
    def next():
        
        QueryStates._id += 1
        
        return str(QueryStates._id)

    @staticmethod
    def parse_query_id(current_id):

        ids = current_id.split('@')
        
        return ids[-1] if len(ids) == 1 else '@'.join(ids[:-1])
        
    @staticmethod
    def store(query, stage_key):
        
        query_id = query['query_id']
        
        QueryStates._memory[stage_key][query_id] = query
    
    @staticmethod
    def read(query_id, stage_key):
             
        return QueryStates._memory[stage_key][query_id]
    
    @staticmethod
    def remove(query_id, stage_key):
        
        del QueryStates._memory[stage_key][query_id]
        
        
# ----------------------------------------------------------------------------------------------------------------------------------------

def next_stage(query: Dict[Any,Any], **kwargs):
    
    command = query['command']
    
    assert 'command' in query , 'command not in the query'
    assert command in Command.main_path , 'command type is not in supported commands'
    
    if 'state_code' in query:
        
        state_code = query['state_code']
        
        return Command.main_path[command][state_code](query, **kwargs)

# ----------------------------------------------------------------------------------------------------------------------------------------

def pure_to_ready(pure_query: Dict[Any,Any]):
    
    #TODO add if none returned
    
    # 1) validate input blocks
    
    query_validation.validate_images_in_pure_query(pure_query)
    ready_query = query_parser.make_ready(pure_query)

    base_gathered_query = query_parser.make_base_of_gathered(ready_query)
    
    QueryStates.store(query=base_gathered_query, stage_key='active_gathered')
    
    next_stage(ready_query)


def specialized_pure_to_ready(pure_query: Dict[Any,Any]):

    tmp = query_validation.ready_check(pure_query)
    
    if tmp is not None:
    
        raise Exception(tmp)

    ready_query = query_parser.make_specialized_ready(pure_query)

    base_gathered_query = query_parser.make_base_of_gathered(ready_query)

    QueryStates.store(query=base_gathered_query, stage_key='active_gathered')

    next_stage(ready_query)

# ----------------------------------------------------------------------------------------------------------------------------------------

def query_to_pure(command: str, inputs: Dict[Any, Any]):

    query_id = QueryStates.next()

    if command == 'predict':
        
        specialized_pure_query = query_parser.make_specialized_pure(query_id, command, inputs)
        
        next_stage(specialized_pure_query)

    return query_id
    
# ----------------------------------------------------------------------------------------------------------------------------------------

def ready_to_ongoing(ready_query: Dict[Any, Any]):

    processed_queries = query_parser.make_processed(ready_query)
    
    for ong in processed_queries:
        
        next_stage(ong)
        
    # with ThreadPoolExecutor(max_workers=None) as executer:
    #     executer.map(next_stage, processed_queries)

# ----------------------------------------------------------------------------------------------------------------------------------------

def ongoing_to_preprocessing(on_going_query: Dict[Any,Any]):
    
    query_preprocess.preprocess_ongoing_query(on_going_query)
    
    on_going_query['stage'] += 1
    
    next_stage(on_going_query)


# ----------------------------------------------------------------------------------------------------------------------------------------

def preprocessing_to_gathered(on_going_query: Dict[Any,Any]):

    query_id = QueryStates.parse_query_id(current_id=on_going_query['query_id'])

    gathered = QueryStates.read(query_id=query_id, stage_key='active_gathered')

    new_gathered = query_parser.insert_into_gathered(on_going_query, gathered)

    next_stage(new_gathered)
    
# ----------------------------------------------------------------------------------------------------------------------------------------

def ongoing(on_going_query: Dict[Any,Any]):

    sub_stages = [ongoing_to_preprocessing , preprocessing_to_gathered]

    assert 'stage' in on_going_query

    sub_stages[on_going_query['stage']](on_going_query)

# ----------------------------------------------------------------------------------------------------------------------------------------

def gathered_ready(gathered_query: Dict[Any,Any]):

    gathered_query['stage'] = 2

    QueryStates.store(query=gathered_query, stage_key='ready_gathered')
    QueryStates.remove(query_id=gathered_query['query_id'], stage_key='active_gathered')

    next_stage(gathered_query)

# ----------------------------------------------------------------------------------------------------------------------------------------

def gathered_to_ai(gathered_query: Dict[Any,Any]):

    finished_query = query_predict.predict(gathered_query=gathered_query)
    finished_query['state_code'] += 1

    next_stage(finished_query)
    
# ----------------------------------------------------------------------------------------------------------------------------------------

def gathered(gathered_query:Dict[Any,Any]):
    
    # case: gathered no ready
    if gathered_query['stage'] == 0:
        
        return
    
    sub_stages = [gathered_ready, gathered_to_ai]
    
    assert 'stage' in gathered_query

    sub_stages[gathered_query['stage'] - 1](gathered_query)

# ----------------------------------------------------------------------------------------------------------------------------------------

def make_finalized_query(finished_query: Dict[Any, Any]):
    
    # finished_query['content'][spec]['outputs'] -> ('data', 'tags')
    
    query_outputs = []
    
    for spec in finished_query['content']:
        
        outputs = finished_query['content'][spec]['outputs']
        
        query_outputs.append(outputs)
    
    finalized_query = {'query_id': finished_query['query_id'], 
                       'state_code': finished_query['state_code'] + 1, 
                       'outputs': query_outputs}
    
    QueryStates.store(finalized_query, stage_key='finalized')
    
# ----------------------------------------------------------------------------------------------------------------------------------------

def execute_specialized_quest_query(command: str, inputs: Dict[Any, Any]):
    
    query_id = query_to_pure(command=command, inputs=inputs)

    finalized_query = QueryStates.read(query_id=query_id, stage_key='finalized')
    
    return finalized_query['outputs']
