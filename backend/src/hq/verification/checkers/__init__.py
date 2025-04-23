from .. import query


def register_query_checker(fn):
    
    query.CHECKERS[fn.__name__] = fn
    
@register_query_checker
def min_cardinality(a, value):
    
    return len(a) >= value

@register_query_checker
def max_cardinality(a, value):
    
    return len(a) <= value
