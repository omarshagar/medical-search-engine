from typing import Dict, Any, List

from PyQt5 import QtCore

from ..types.abstract import ListModel

class OutputStatus:
    
    Free = 0
    Ready = 1
    
class OutputModel(ListModel):
    
    Roles = ['tags', 'status', 'data']
    
    # [Signals] ==========================================================
    activeIndexChanged = QtCore.pyqtSignal(int)
   
    def __init__(self, roles=None, parent=None):
        
        if roles is None:
            
            roles = OutputModel.Roles
                        
        super(OutputModel, self).__init__(roles=roles, parent=parent)

        self._active_index = -1

    @QtCore.pyqtProperty(int, notify=activeIndexChanged)
    def activeIndex(self):
        
        return self._active_index
    
    @activeIndex.setter
    def activeIndex(self, index):

        self._active_index = index
        self.activeIndexChanged.emit(index)
         
    @QtCore.pyqtSlot(list)
    def reset(self, outputs: List[Dict[Any, Any]]):
        
        self.removeAll()
        
        # TODO: must be sorted based on block_index
        for ith_output in outputs:
            
            for block_index in ith_output:
                
                content = ith_output[block_index]
                
                certainty = content['certainty']
                tags: List[Any] = content['tags'] + [certainty]
                data = content['data'] if 'data' in content else None
                
                if content['is_stream']:
                    
                    tags.append('stream') 
                    
                item = {'type': content['type'], 'tags': tags, 'data': data, 'status': OutputStatus.Ready}

                self.append(item)
            
    @QtCore.pyqtSlot(int, int, result=QtCore.QVariant)
    def getColumn(self, index, column):
        
        data = self.getRole(index, 'data')
        
        if not (0 <= column < len(data)):
            
            return 0
            
        return data[column]
    
    @QtCore.pyqtSlot(int, result=int)
    def columnCount(self, index):
        
        data = self.getRole(index, 'data')
        
        if data is None:
            
            return 0
        
        return len(data)
