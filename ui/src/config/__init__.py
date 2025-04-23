import os
import glob
from pathlib import Path

import copy

from .. import utils

from backend import graph_utils, ReadOnlyDict
from backend import config as backend_config


class Config:
        
    working_dir = Path(__file__).parent.parent.parent

    Icons = {utils.parse_filename(path): path for path in glob.glob(os.path.join(working_dir, 'images/icon/*.png'))}
    
    specialized_quest_types = backend_config.Config.specialized_quest_types
    profile = backend_config.Config.models
    
    invalid_specialized_quest = {'all_specs'}
    
    loader_filters = {'image': ['*.png', '*.jpeg', '*.jpg']}
    
    loader_checkers = {'image': utils.is_image}

    report_header_keys = ['title', 'created_at']
    report_delta_time = 1000
    
    @staticmethod
    def get_specialization_items_dictionary(default=None, childs_key='childs'):
        
        if default is None:
            
            default = {'selected': False, 'status': 1}
        
        items_dictionary = {}
        
        visited = set()
        
        for parent in Config.specialized_quest_types:
            
            if parent in visited:
                
                continue
            
            if parent not in Config.invalid_specialized_quest:
                
                icon_url = Config.Icons[parent] if parent in Config.Icons else Config.Icons['missing']
                
                items_dictionary[parent] = {'name': parent, 'iconUrl': icon_url}
                items_dictionary[parent].update(default)
            
            visited.add(parent)
            
            if childs_key is None:

                childs = Config.specialized_quest_types[parent]
            
            else:

                childs = Config.specialized_quest_types[parent][childs_key]

            for node in childs:
                
                if node in visited:
                
                    continue
                
                if node not in Config.invalid_specialized_quest:

                    icon_url = Config.Icons[node] if node in Config.Icons else Config.Icons['missing']

                    items_dictionary[node] = {'name': node, 'iconUrl': icon_url}
                    items_dictionary[node].update(default)

                visited.add(node)

        return ReadOnlyDict(items_dictionary)


    @staticmethod
    def get_clustered_reference():

        clustered_reference = graph_utils.cluster_by_level(Config.specialized_quest_types, has_cycle=False, childs_key='childs')
                  
        return ReadOnlyDict(clustered_reference)

    @staticmethod
    def get_query_item(profile_id, default=None):

        profile = copy.deepcopy(Config.profile[profile_id])
  
        if default is None:
        
            default = {'selected': False, 'status': 1, 'data': None}
                
        iconUrl = Config.Icons[profile['icon_name']]
        
        item = {'title': profile['title'], 'profile': profile, 'iconUrl': iconUrl}
        item.update(default)
        
        return item
    
    @staticmethod
    def get_report_item(report_id, profile_id, default=None):
        
        profile = copy.deepcopy(Config.profile[profile_id])
        
        if default is None:
        
            default = {'status': 1}
        
        placeholderType = "image"        
        placeholderUrl = Config.Icons['xreport']
        header = {'title': profile['title'], 'created_at': utils.get_utc_time()}
                
        report = {'report_id': report_id, 'profile': profile, 'placeholderType': placeholderType,
                  'placeholderUrl': placeholderUrl, 'header': header}
        
        report.update(default)
        
        return report

        
