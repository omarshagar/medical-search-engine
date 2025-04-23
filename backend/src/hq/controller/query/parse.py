import copy
from typing import List, Set, Dict, Any

from collections import defaultdict
import concurrent.futures

from ...utils import graph
from ...verification import query

from ...config import Config

# from ...tracer import pipeline as tracer


### @
def get_models_depending_on_specializations(specializations: Set):
    
    all_specs = Config.specialized_quest_types
    
    ids = set()
    
    for spec in specializations:
    
        if len(all_specs[spec]['model_ids']) > 0:
        
            ids.update(all_specs[spec]['model_ids'])
            
        for sub_spec in graph.make_dfs_iterator(graph=Config.specialized_quest_types, has_cycle=False, start_node=spec, childs_key='childs'):
            
            if len(all_specs[sub_spec]['model_ids']) > 0:
        
                ids.update(all_specs[sub_spec]['model_ids'])     

    return ids

### @
def make_pure(query_id: str, command: str, inputs: Dict[Any, Any]) -> Dict[Any, Any]:
    
    """Convert inputs and refrence tree(tree of specializations) to pure query(first shape of the query)

    Args:
        query_id: id of the query
        command: predict
        inputs: for predict command

            inputs['specialization']='some_spec_in_refrence_tree'
            inputs['types'] = ['image','text','signal']
            inputs['image'] = ['subtype']
            inputs['subtype'] = ['name']
            inputs['name'] = ['path/of/an/image/']

    Returns: Pure qury

    """
    reference = Config.specialized_quest_types
    pure_query={}
    pure_query["inputs"]=inputs.copy()
    pure_query["specializations"]={}

    #take the sub-specialization name
    allspecs = inputs['specialization']
    for spec in allspecs:
    # this line should never be true, and just being used for debugging (can be removed in the release version)
        assert spec in reference, 'Some nodes are not contained in the reference graph or the query graph is invalid'
        #coby the subtree of refrence into pure_query["specializations"]
        for ref_key in graph.make_bfs_iterator(reference, has_cycle=False, start_node=spec , childs_key='childs'):
            pure_query["specializations"][ref_key] = []
            for child in reference[ref_key]['childs']:
                # append node, if it is candidate child
                pure_query["specializations"][ref_key].append(child)

    pure_query['state_code'] = 0
    pure_query['query_id'] = query_id
    pure_query['command'] = command
    
    return pure_query


### @
def make_specialized_pure(query_id: str, command: str, inputs: Dict[Any, Any]) -> Dict[Any, Any]:
    """Convert inputs and refrence tree(tree of specializations) to pure query(first shape of the query)

    Args:
        query_id: id of the query
        command: predict
        inputs: for predict command


    Returns: Specialized Pure qury

    """
    specialized_pure_query = {}
    specialized_pure_query['state_code'] = 0
    specialized_pure_query['query_id'] = query_id
    specialized_pure_query['command'] = command
    specialized_pure_query["content"] = copy.deepcopy(inputs["content"])

    return specialized_pure_query

### @
def validate_txts_in_pure_query(pure_query: Dict[Any, Any])->bool:
    
    raise NotImplementedError()


### @
def validate_signals_in_pure_query(pure_query: Dict[Any, Any])->bool:
    
    raise NotImplementedError()

### @
def is_valid_model_depending_on_input(model_input: Dict[Any, Any], pure_query_input: Dict[Any, Any] )->bool:
    
    check_fields = ['type', 'subtype', 'name']
    
    model_data = []
    
    for field in check_fields:
    
        assert field in model_input , "field name not in model_input"

        model_data.append(model_input[field])
        
    for i in range(len(check_fields)):
        
        if model_data[i] not in pure_query_input:
        
            return False
        
        if i > 0 and model_data[i] not in pure_query_input[model_data[i - 1]]:
        
            return False
        
    return True


### @
def get_valid_models_depending_on_input(pure_query: Dict[Any, Any]) -> Dict[Any,Any]:
    
    models = []
    
    for sub_spec in pure_query['inputs']['specialization']:
        
        for node in graph.make_dfs_iterator(pure_query['specializations'], False, sub_spec, False):
            
            if node in Config.specialized_quest_types and len(Config.specialized_quest_types[node]["model_ids"]) > 0 :
            
                for model_id in Config.specialized_quest_types[node]["model_ids"]:
            
                    models.append([model_id,node])


    ready = {}
    
    #we have problem of : what if one spec have multi model ?
    #I will create multible spec as spec@1 , spec@2....
    sub_spec_count={}
    
    for model,sub_specialization in models:
    
        url_start = {}
    
        model_inputs = Config.models[model]['inputs']
        valid_model = 1
        
        inputs=[]
        
        for m_input in model_inputs:
        
            #edit this to make it only graph
            m_name = m_input['name']
        
            if is_valid_model_depending_on_input(m_input,pure_query['inputs']):
        
                if m_name not in url_start:
        
                    url_start[m_name] = 0
        
                if url_start[m_name] < len(pure_query['inputs'][m_name]):
        
                    url = pure_query['inputs'][m_name][url_start[m_name]]
                    url_start[m_name] += 1
        
                    single_input = {}
                    
                    single_input['block_index'] = m_input['block_index']
                    single_input['url'] = url
        
                    inputs.append(single_input)
        
                else:
        
                    valid_model = 0
        
            else:
        
                valid_model = 0
        
            if not valid_model:
        
                break
        
        if valid_model:
        
            if sub_specialization not in sub_spec_count:
        
                sub_spec_count[sub_specialization] = 0
        
            sub_spec_count[sub_specialization] +=1
        
            name = sub_specialization
            name += '@'
            name += str(sub_spec_count[sub_specialization])
        
            ready[name] = {}
            ready[name]["model_id"] = model
            ready[name]["inputs"] = []
            ready[name]["inputs"] = inputs
            
    return ready


### @
def make_ready(pure_query: Dict[Any, Any]) -> Dict[Any, Any]:
    
    """create ready_query
        steps of converting pure to ready :
        2-remove models that not compatible with input
        3-verify that there is any valid model
        4-connect models with input

    Args:
        pure_query:
    Returns:
        ready_query:
            with this form (config/queries/structure.json):
    """
    semi_ready = get_valid_models_depending_on_input(pure_query)
    
    ready_query = {}
    ready_query['content'] = semi_ready
    ready_query['state_code'] = 1
    ready_query['command'] = pure_query['command']
    ready_query['query_id'] = pure_query['query_id']
    
    make_base_of_gathered(ready_query)
    
    return ready_query


def make_specialized_ready(pure_query: Dict[Any, Any]) -> Dict[Any, Any]:
    """create ready_query
        steps of converting pure to ready :
        2-remove models that not compatible with input
        3-verify that there is any valid model
        4-connect models with input

    Args:
        pure_query:
    Returns:
        ready_query:
            with this form (config/queries/structure.json):
    """

    ready_query = {}
    ready_query['state_code'] = 1
    ready_query['command'] = pure_query['command']
    ready_query['query_id'] = pure_query['query_id']
    ready_query['content'] = {'any_spec':{}}
    spec = ready_query['content']['any_spec']
    spec['model_id'] = pure_query['content']['model_id']
    spec['inputs'] = []
    inputs = spec['inputs']
    content = pure_query['content']

    for  node,parent in graph.make_dfs_iterator(content, has_cycle=False, return_parent=True, start_node='types'):
        
        if node not in content:
            
            inputs.append({"block_index": parent, "url": node})

    return ready_query


### @
def make_base_of_gathered(ready_query: Dict[Any,Any]):

    """It creates the base of gathered query by settiong the file in FileSystem/queries/gatheredQueries
        it will be moved to ready when "recieved_input" == "total_inputs"

    Args:
        ready_query:

    Returns:NONE

    """

    gathered = copy.deepcopy(ready_query)

    gathered["state_code"] = 3
    gathered["stage"] = 0
    gathered["total_inputs"] = 0
    gathered["recieved_input"] = 0

    for spec in gathered['content']:

        gathered["total_inputs"] += len(gathered['content'][spec]['inputs'])

    return gathered


### @
def cluster_inputs_of_all_models_preprocessing(ready_query: Dict[Any,Any]) -> Dict[Any,Any]:
    
    clustred_data = {}
    
    all_specs = ready_query['content']
    models_conf = Config.models
    
    for spec_name, spec_data in all_specs.items():
    
        model_name = spec_data['model_id']
        model_conf = models_conf[model_name]['metadata']
        preprocess = model_conf['preprocessing']

        # types = model_conf['inputs']
        inputs_related_to_model = spec_data['inputs']

        for input in inputs_related_to_model:
            
            preprocessing_data = preprocess[input['block_index']]
            
            tmp = copy.deepcopy(preprocessing_data)
            tmp.pop('block_index')
            
            pre = sorted(tmp.items())
            pre = str(pre)
            
            if pre not in clustred_data:
                
                clustred_data[pre] = [[], []]
            
            meta_of_cur_input = {}
            
            meta_of_cur_input["specialization"] = spec_name
            meta_of_cur_input["model"] = model_name
            meta_of_cur_input["block_index"] = input['block_index']

            clustred_data[pre][0].append(meta_of_cur_input)
            clustred_data[pre][1].append(input["url"])
            
    return clustred_data


### @
def make_processed(ready_query: Dict[Any, Any]) -> Dict[Any, Any]:
    
    """

    Args:
        ready_query:

    Returns:
        Group of processed queries
    """
    
    clustered_data = cluster_inputs_of_all_models_preprocessing(ready_query)
    
    template = {}
    
    template["state_code"] = 2
    template["stage"] = 0
    template["command"] = ready_query['command']
    template["query_id"] = ready_query["query_id"]
    template["path_length"] = 0
    
    # TODO: remove predefined category
    template["category"] = "image"
    template["metadata"] = []
    template["files_urls"] = []
    template["data"] = []
    
    on_going = {}
    on_going['queries'] = []
    
    cnt = 0
    
    for cluster in clustered_data.values() :
        
        processed = copy.deepcopy(template)
        
        processed["query_id"] += ('@' + str(cnt))
        processed["metadata"] = cluster[0]
        processed["files_urls"] = cluster[1]
        
        on_going["queries"].append(processed)
        
        cnt += 1

    #TODO add concurrency
    # for q in on_going['queries']:
    #     tracer.next_stage(q)
    # with concurrent.futures.ThreadPoolExecutor() as executer:
    #     results=executer.map(tracer.next_stage,OnGoing['queries'])
    #     TODO add what if failed?
    
    return on_going['queries']


### @
def insert_into_gathered(ongoing_query: Dict[Any, Any], gathered: Dict[Any, Any]):

    for i in range(len(ongoing_query['metadata'])):
        
        metadata = ongoing_query['metadata'][i]
        specialization = metadata['specialization']
        model_id = metadata['model']
        block_idx = metadata['block_index']
        url = ongoing_query['files_urls'][i]
        data = ongoing_query['data'][i]

        inserted = False
        
        for g_spec, g_body in gathered['content'].items():
        
            g_model = g_body['model_id']
        
            if (g_spec == specialization) and (g_model==model_id):
                
                for g_input in g_body['inputs']:
                
                    if (url == g_input['url']) and (block_idx == g_input['block_index']) and ('data' not in g_input):
                
                        g_input['data'] = data
                        gathered["recieved_input"] += 1
                        
                        inserted = True
                
                        break

            if inserted:
                
                break

        #gathered['metadata'][spec]['inputs'].append()[idx]['url'] = ongoing_query['new_urls'][i]
        
    if gathered['recieved_input'] == gathered['total_inputs']:
        
        gathered["stage"] = 1

    return gathered


### @
def make_finished(processed_query: Dict[Any, Any], finished_config: Dict[Any, Any]) -> Dict[Any, Any]:

    raise NotImplementedError()


### @
def make_sorted(queries: List[Dict[Any, Any]], keys: List[Any]) -> List[Dict[Any, Any]]:

    raise NotImplementedError()


### @
def group_by(queries: List[Dict[Any, Any]], by: List[Any]) -> List[Dict[Any, Any]]:

    raise NotImplementedError()
