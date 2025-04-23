from ..controller.query import parse

from . import pipeline
from ..verification import checkers

# pipeline.Command.register(fn=pipeline.pure_to_ready, key='predict', index=0)
# pipeline.Command.register(fn=pipeline.ready_to_ongoing, key='predict', index=1)
# pipeline.Command.register(fn=pipeline.ongoing, key='predict', index=2)
# pipeline.Command.register(fn=pipeline.gathered, key='predict', index=3)

# pipeline.Command.register(fn=pipeline.AI_to_postprocessing, key='predict', index=2)
# pipeline.Command.register(fn=pipeline.postprcessing_to_output, key='predict', index=3)


pipeline.Command.register(fn=pipeline.specialized_pure_to_ready, key='predict', index=0)
pipeline.Command.register(fn=pipeline.ready_to_ongoing, key='predict', index=1)
pipeline.Command.register(fn=pipeline.ongoing, key='predict', index=2)
pipeline.Command.register(fn=pipeline.gathered, key='predict', index=3)
pipeline.Command.register(fn=pipeline.make_finalized_query, key='predict', index=4)

def get_models_id(selected_specializations):
    
    return parse.get_models_depending_on_specializations(selected_specializations)


