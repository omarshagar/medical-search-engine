import queue
from typing import Callable, Set, Dict, Any, Iterator

from collections import deque


def get_common(query: Dict[Any, Any], reference: Dict[Any, Any]) -> Set[Any]:
    """ Get common nodes keys of query & reference graphs

        Args:
            query (Dict[Any, Any]): first graph
            reference (Dict[Any, Any]): second graph

        Return:
            Set[Any] : set of all common nodes

    """

    return query.keys() & reference.keys()


# noinspection DuplicatedCode
def make_dfs_iterator(graph: Dict[Any, Any], has_cycle: bool = False, start_node: Any = None, return_parent=False, 
                      childs_key=None, condition: Callable = None) -> Iterator[Any]:

    if start_node is None:

        start_node = get_roots(graph=graph, childs_key=childs_key)

    visited = None
    parent = None

    if has_cycle:

        visited = set()

    if return_parent:

        stack = deque([(start_node, parent)])

    else:

        stack = deque([start_node])

    while stack:

        if return_parent:

            (node, parent) = stack.popleft()

        else:

            node = stack.popleft()

        if has_cycle:

            if node in visited:

                continue

            visited.add(node)

        if return_parent:

            yield node, parent

        else:

            yield node

        if node not in graph:

            continue

        # condtion at which child key should be ignored (not inserted to DFS stack)
        if (condition is not None) and not condition(node):
            
            continue
                    
        childs = []
        
        if childs_key is None:

            childs = graph[node]
        
        else:

            childs = graph[node][childs_key]

        for child in childs:
                                
            if return_parent:

                stack.appendleft((child, node))

            else:

                stack.appendleft(child)


# noinspection DuplicatedCode
def make_bfs_iterator(graph: Dict[Any, Any], has_cycle: bool = False,
                      start_node: Any = None, return_parent=False, childs_key=None) -> Iterator[Any]:


    if start_node is None:

        start_node = get_roots(graph=graph, childs_key=childs_key)
        
    visited = None
    parent = None

    if has_cycle:

        visited = set()

    if return_parent:

        queue = deque([(start_node, parent)])

    else:

        queue = deque([start_node])

    while queue:

        if return_parent:

            (node, parent) = queue.popleft()

        else:

            node = queue.popleft()

        if has_cycle:

            if node in visited:

                continue

            visited.add(node)

        if return_parent:

            yield node, parent

        else:

            yield node

        if graph[node] is None:

            continue

        childs=[]

        if childs_key is None:
        
            childs = graph[node]
        
        else:
        
            childs = graph[node][childs_key]
        
        for child in childs:

            if child not in graph:

                continue

            elif return_parent:

                queue.append((child, node))

            else:

                queue.append(child)


def get_spec(graph: Dict[Any, Any], childs_key=None):
    
    spec = {}
    
    for parent in graph:
        
        if parent not in spec:
            
            spec[parent] = {'in_degree': 0, 'out_degree': 0}
        
        spec[parent]['out_degree'] = len(graph[parent])
        
        if childs_key is None:

            childs = graph[parent]

        else:

            childs = graph[parent][childs_key]

        for node in childs:
                
            if node not in spec:
                
                spec[node] = {'in_degree': 0, 'out_degree': 0}
                            
            spec[node]['in_degree'] += 1
    
    return spec


def get_roots(graph: Dict[Any, Any], childs_key=None):
        
    spec = get_spec(graph, childs_key=childs_key)
    
    for key in spec:
        
        if spec[key]['in_degree'] == 0:
            
            yield key


def get_at(graph: Dict[Any, Any], depth: int, has_cycle: bool = False, childs_key=None):
    
    roots = list(get_roots(graph, childs_key=childs_key))
    roots_level = [0] * len(roots)
    
    stack = deque(list(zip(roots, roots_level)))
    
    visited = None
    
    if has_cycle:
        
        visited = set()
    
    while len(stack):
        
        (node, level) = stack.popleft()
        
        if has_cycle:
            
            if node in visited:
                
                continue
                
            visited.add(node)
        
        if level > depth:
        
            continue
        
        elif level == depth:
            
            yield node
        
        if childs_key is None:

            childs = graph[node]
        
        else:

            childs = graph[node][childs_key]

        for child in childs:
            
            # if the node is a leaf-node
            if child not in graph:
                
                continue
            
            stack.appendleft((child, level + 1))

def reduce_any(graph: Dict[Any, Any], condition_fn: Callable, has_cycle: bool = False, childs_key=None):
    
    all_roots = list(get_roots(graph, childs_key=childs_key))

    valid_roots = []
    
    for root in all_roots:
        
        if condition_fn(root):
            
            valid_roots.append(root)

    stack = deque(valid_roots)
    
    taken = set()
    
    visited = None
    
    if has_cycle:
        
        visited = set()
    
    while len(stack):
        
        node = stack.popleft()
        
        if has_cycle:
            
            if node in visited:
                
                continue
                
            visited.add(node)

        if childs_key is None:

            childs = graph[node]
        
        else:

            childs = graph[node][childs_key]
                
        for child in childs:
            
            child_state = condition_fn(child)
                        
            # if the node is a leaf-node
            if child not in graph:
                
                if child_state:
                    
                    taken.add(child)
                                        
                continue
            
            if not child_state:
                            
                continue
                                       
            stack.appendleft(child)

        taken.add(node)
            
    return taken

def cluster_by_level(graph: Dict[Any, Any], has_cycle: bool = False, childs_key=None):
    
    out_graph = {}
    
    roots = list(get_roots(graph, childs_key=childs_key))
    roots_level = [0] * len(roots)

    queue = deque(list(zip(roots, roots_level)))
    
    visited = None
    
    if has_cycle:
        
        visited = set()
    
    while len(queue):
        
        (node, level) = queue.popleft()
        
        if has_cycle:
            
            if node in visited:
                
                continue
                
            visited.add(node)
        
        if level not in out_graph:
            
            out_graph[level] = {}
        
        out_graph[level][node] = []
        
        if childs_key is None:

            childs = graph[node]
        
        else:

            childs = graph[node][childs_key]

        for child in childs:

            out_graph[level][node].append(child)
                 
            # if the node is a leaf-node
            if child not in graph:
                
                continue
            
            queue.append((child, level + 1))

    return out_graph


def contain_cycle(graph: Dict[Any, Any]) -> bool:

    raise NotImplementedError()


def is_tree(graph: Dict[Any, Any]) -> bool:
    """

    Args:
        graph:

    Returns:
        bool : if graph tree or not
    """
    in_deg={}
    for v in graph:
        if v not in in_deg:
            in_deg[v]=0
        for child in graph[v]:
            if child not in in_deg:
                in_deg[child]=0
            in_deg[child]+=1
    cnt={0:0 ,1:0}
    for v,deg in in_deg.items():
        if deg not in cnt:
            return False
        cnt[deg]+=1
    if cnt[0]==1:
        return True
    return False


def filter_pure_query_depending_on_links(pure_query:Dict[Any,Any],cur_node='types',parent='inputs'):
    """recursive function that removes all nodes in pure query that has not childs

    Args:
        cur_node:
        pure_query:

    Returns:
        number of all files in input
    """
    if cur_node not in pure_query['inputs']:
        return 1

    cnt = 0
    for child in pure_query['inputs'][cur_node]:
        cnt += filter_pure_query_depending_on_links(pure_query,child,cur_node)

    if cnt == 0:
        pure_query['inputs'].pop(cur_node)
    return cnt





def is_subgraph(graph: Dict[Any, Any], reference: Dict[Any, Any]) -> bool:

    raise NotImplementedError()
