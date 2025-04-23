from json import load
from typing import Dict, Any, List
import copy

from PyQt5 import QtCore

from backend import config as backend_config

from ..types.abstract import ListModel
from ..config import Config


class InputStatus:
    
    Free = 0
    Ready = 1
    Loading = 2
    Loaded = 3
    Successed = 4
    Faild = -1

class WorkerStatus:
    
    active = False
    count = 0
    
class InputModel(ListModel):
    
    Roles = ['tags', 'status', 'data', 'loader_info']
    
    # [Signals] ==========================================================
    activeIndexChanged = QtCore.pyqtSignal(int)
    columnChanged = QtCore.pyqtSignal(int, bool) # (old_column_count, push/pop)
   
    def __init__(self, roles=None, parent=None):
        
        if roles is None:
            
            roles = InputModel.Roles
                        
        super(InputModel, self).__init__(roles=roles, parent=parent)
    
        self._active_index = -1
        
    @QtCore.pyqtProperty(int, notify=activeIndexChanged)
    def activeIndex(self):
        
        return self._active_index
    
    @activeIndex.setter
    def activeIndex(self, index):

        self._active_index = index
        self.activeIndexChanged.emit(index)
        
    @QtCore.pyqtSlot(int, QtCore.QVariant, result=int)
    def setData(self, index, data: List[QtCore.QUrl]):
        
        loader_info = self.getRole(index, 'loader_info')
        _data = self.getRole(index, 'data')
        _is_valid = self.getRole(index, 'is_valid')
        
        if _data is None:
            
            _data = []
        
        if _is_valid is None:
            
            _is_valid = []
            
        min_count = loader_info['min_count']
        max_count = loader_info['max_count']

        typ = loader_info['type']
        
        if loader_info['loaded_count'] == max_count:
            
            return 0
                    
        elif max_count < len(data):
                        
            state = max_count - len(data)
                    
            data = data[:max_count]
        
        else:
            
            state = len(data)
            
        loader_info['loaded_count'] += len(data)

        is_valid = []
        
        for i in range(len(data)):

            is_valid.append(Config.loader_checkers[typ](data[i].path()))
                    
        _data.extend(data)
        _is_valid.extend(is_valid)
            
        self.updateRole(index, 'loader_info', loader_info)
        self.updateRole(index, 'data', _data)
        self.updateRole(index, 'is_valid', _is_valid)
        
        if loader_info['loaded_count'] >= min_count:
            
            self.updateRole(index, 'status', InputStatus.Ready)
        
        else:
            
            self.updateRole(index, 'status', InputStatus.Loading)

        old_count = loader_info['loaded_count'] - len(data)
        
        self.columnChanged.emit(old_count, True)
        
        return state
    
    @QtCore.pyqtSlot(list)
    def reset(self, inputs_metadata: List[Dict[Any, Any]]):
        
        self.removeAll()
        
        for ith_input in inputs_metadata:
            
            _type = ith_input['type']
            
            assert _type in Config.loader_filters, 'Invalid data-type'
            
            tags = backend_config.Metadata.get_tags(ith_input)
            
            if ith_input['is_stream']:
                
                tags.append('stream') 
                
            item = {'tags': tags, 'status': InputStatus.Free, 'data': None, 'is_valid': None,
                    'loader_info': {'type': ith_input['type'], 
                                    'filters': Config.loader_filters[_type],
                                    'min_count': ith_input['min_cardinality'], 
                                    'max_count': ith_input['max_cardinality'], 
                                    'loaded_count': 0}, 'metadata': ith_input}

            self.append(item)

    @QtCore.pyqtSlot(int, int, result=QtCore.QVariant)
    def getColumn(self, index, column):
        
        if not (0 <= column < self.columnCount(index)):
            
            return None
        
        data = self.getRole(index, 'data')
    
        return data[column]
    

    @QtCore.pyqtSlot(result=dict)
    def getInputsState(self):
        
        """
        - verify that the expected count is zero for all items 
        - check if all data are valid (is_valid property is true for all)
        """
        
        state = {'remaining_count': 0, 'all_valid': True}
        
        for item in self.items:
            
            state['remaining_count'] += max(0, item['loader_info']['min_count'] - item['loader_info']['loaded_count'])
            
            if item['is_valid'] is not None:
                
                state['all_valid'] &= all(item['is_valid'])
        
        return state
      
    @QtCore.pyqtSlot(int, result=int)
    def columnCount(self, index):
        
        data = self.getRole(index, 'data')
        
        if data is None:
            
            return 0
                
        return len(data)

    @QtCore.pyqtSlot(int, int)
    def removeColumn(self, index, column):
        
        loader_info = self.getRole(index, 'loader_info')
        data = self.getRole(index, 'data')
        is_valid = self.getRole(index, 'is_valid')
                
        if not (0 <= column < self.columnCount(index)):
            
            return -1
            
        data.pop(column)
        is_valid.pop(column)
        
        loader_info['loaded_count'] -= 1
        
        self.updateRole(index, 'loader_info', loader_info)
        self.updateRole(index, 'data', data)
        self.updateRole(index, 'is_valid', is_valid)
        
        if len(data) == 0:
            
            self.updateRole(index, 'status', InputStatus.Free)
        
        elif len(data) >= loader_info['min_count']:
            
            self.updateRole(index, 'status', InputStatus.Ready)
        
        else:
            
            self.updateRole(index, 'status', InputStatus.Loading)

        old_count = loader_info['loaded_count'] + 1
        
        self.columnChanged.emit(old_count, False)

        return 1
    
    @QtCore.pyqtSlot(int, int, result=str)
    def getPath(self, index, column):
        
        url = self.getColumn(index, column)
        
        if url is None:
            
            return None
            
        return url.path()

    def toSpecializedQuestGraph(self, model_id):
        
        content_graph = {'model_id': model_id}
        
        keys = zip(['types'] + backend_config.Metadata.tag_keys, backend_config.Metadata.tag_keys + ['data'])
        keys = list(keys)
        
        for parent_key, child_key in keys:
            
            for item in self.items:
                
                metadata = item['metadata']
                
                node = metadata[parent_key] if parent_key in metadata else parent_key
                
                if node not in content_graph:
                    
                    content_graph[node] = []
                
                if child_key == 'data':
                    
                    block_index = metadata['block_index']
                    data = [url.path() for url in item[child_key]]
                    
                    content_graph[node].append(block_index)
                    content_graph[block_index] = data
                
                else:
                    
                    content_graph[node].append(metadata[child_key])

        return {'content': content_graph}
    
    @QtCore.pyqtSlot()
    def clone(self) -> 'InputModel':

        instance = InputModel(roles=self.roles)
        
        for item in self.items:
            
            new_item = {}
            
            for key, value in item.items():
                
                if key == 'data':
                    
                    new_item[key] = [QtCore.QUrl(copy.deepcopy(url.path())) for url in item['data']]
                    
                else:
                    
                    new_item[key] = copy.deepcopy(value)
                
            # should use deepcopy instead           
            instance.append(new_item)
                
        return instance
        