from collections import deque

import numpy as np


SEED = 0
NAMES = [chr(code) for code in range(ord('A'), ord('Z') + 1)]

np.random.seed(SEED)

def random_children(parent=None, max_counts=100):
    
    parent = parent + '/' if parent else ''         
    
    counts = np.random.randint(low=2, high=max_counts)
                
    names = np.random.choice(NAMES, size=counts)
    ids = np.random.randint(low=1, high=counts, size=(counts, ))
    
    nodes = list(map(lambda _name, _id: parent + str(_name) + str(_id), names, ids))
    
    return nodes

def random_graph(max_nodes_per_level=25, max_depth=5, childs_key=None):
    
    out_graph = {}
        
    roots = random_children(max_counts=max_nodes_per_level)

    start_depth = np.random.randint(low=1, high=max_depth+1, size=(len(roots), ))

    start = list(zip(roots, start_depth))    
    
    stack = deque(start)
    
    while stack:
        
        node, depth = stack.popleft()
        
        if node not in out_graph:
            
            out_graph[node] = {childs_key: []} if childs_key else []

                
        if depth == max_depth:            
            
            continue
        
        for child in random_children(parent=node, max_counts=max_nodes_per_level):
            
            stack.appendleft((child, depth + 1))
            
            if childs_key is None:
                
                out_graph[node].append(child)

            else:
                
                out_graph[node][childs_key].append(child)
                
    return out_graph

# print())
