# from src.utils import testing

# graph = testing.build_dummy_graph(depth=3)


# print(graph['A'].children[0]['A'].children[0]['A'].children)


# from src import config as shared_config
# from backend import graph_utils

# for r in graph_utils.get_roots(shared_config.Config.specialized_quest_types):
#     print(r)

# for at in graph_utils.get_at(shared_config.Config.specialized_quest_types, 3):
#     print(at)

# from src.config import Config

# print(Config.get_items_dictionary(default=None))

# from src.shared import virtual_doctors_profiles

# print(virtual_doctors_profiles.get(profile_id='chexpert001').metadata.inputs)

# from ui.src.shared.config import Config

# chexpert001 = Config.profile['chexpert001'].parse()
# print(chexpert001['profile_id'])
# from src.models.inputs import InputModel 

# i = InputModel()
# i.reset(chexpert001['metadata']['inputs'])
# print(i.items)

# from src import utils

# print(utils.local_time_format(utils.get_utc_time()))

# import backend

# from ui.src.shared.config import Config

# print(Config.profile['mura001'].parse())
# print(Config.profile['chexpert001'].parse())

# from backend import tracer

# print(tracer.checkers.query.CHECKERS)

# from ui.src.shared import virtual_doctors_profiles

# virtual_doctors_profiles.to_json(path='./models.json')

from backend import tracer

query = {'content': {'model_id': 'chexpert002', 'types': ['image'], 'image': ['radiograph'], 'radiograph': ['chest'], 'chest': [0], 
                    0: ['/home/m-zayan/Desktop/My-Files/Images/22-Nov-2019 3.jpg', '/home/m-zayan/Desktop/My-Files/Images/22-Nov-2019 2.jpg']}}

ret = tracer.pipeline.execute_specialized_quest_query(command='predict', inputs=query)

print(ret)

# from backend import config
# from backend.src.hq.ai.handlers.chexpert import CheXpert

# model_metadata = config.Config.models['chexpert001']
# print(model_metadata.keys())
# chexpert = CheXpert(model_metadata=model_metadata)
# chexpert.build()
# chexpert.model.summary()    
