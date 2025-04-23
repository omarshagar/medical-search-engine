from typing import Dict, Any

from PyQt5 import QtCore

from ..types.abstract import ListModel

from ..config import Config

# backend imports -----------------------------------------

from backend import tracer, graph_utils

# ---------------------------------------------------------

class SpecializedQuestState:
    
    Idle = 0
    Loading = 1

class SpecializedQuestModel(ListModel):
    
    base_level = 1
    
    reference: Dict[int, Dict[Any, Any]] = Config.get_clustered_reference()
    items_dictionary: Dict[str, Any] = Config.get_specialization_items_dictionary(default=None).copy()
    
    path = {}
    
    # ================================================================
    onStateChanged = QtCore.pyqtSignal(bool)
    isLevelChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, roles, parent=None):
        
        super(SpecializedQuestModel, self).__init__(roles=roles, parent=parent)
        
        self._current_level: int = SpecializedQuestModel.base_level        
        self._state: SpecializedQuestState = SpecializedQuestState.Idle
        
        self.query_model = None
    
    def set_query_model(self, query_model):
        
        self.query_model = query_model
        
    @QtCore.pyqtProperty(int, notify=isLevelChanged)
    def level(self):
        
        return self._current_level
    
    @level.setter
    def level(self, level):
        
        if level != self._current_level:
                
            self._current_level = level
            self.isLevelChanged.emit(True)    

        else:
            
            self.isLevelChanged.emit(False)
            
    @QtCore.pyqtProperty(int, notify=onStateChanged)
    def state(self):
        
        return self._state
    
    @QtCore.pyqtSlot(int)
    def setState(self, state):
        
        if state != self._state:
            
            self._state = state
            self.onStateChanged.emit(True)
        
        else:
                
            self.onStateChanged.emit(False)
                   
    @QtCore.pyqtSlot(int, int)
    def setStatus(self, index, status):
        
        self.updateRole(index, 'status', status)

    @QtCore.pyqtSlot(int, bool)
    def nextCheckState(self, index, state):
        
        self.updateRole(index, 'selected', state)
    
    @QtCore.pyqtSlot(result=bool)
    def isTop(self):
        # the current node has no parent (top level)
        return self.level == SpecializedQuestModel.base_level

    @QtCore.pyqtSlot(result=int)
    def next(self):
        
        self.setState(SpecializedQuestState.Loading)
        
        """
        Returns: 
            -1, 0, or 1
        """
        
        has_selected = False
        has_next = False
        
        for item in self.items:
            
            if item['selected'] and item['status'] == 1:
            
                has_selected = True

                key = item['name']
                
                assert key in SpecializedQuestModel.reference[self.level], f'Invalid graph structure, key={key} does not exist (1)'

                for child in SpecializedQuestModel.reference[self.level][key]:
                
                    if child not in Config.invalid_specialized_quest:
                    
                        has_next = True
                        
                        break
                    

        # if user does not select any item, provide a message & do nothing
        if not has_selected:
        
            return -1

        # if the current level contains only leafs, provide a message & do nothing
        elif not has_next:
            
            return 0
        
        children = []
        
        # path buffer to be used for backtracking
        if self.level not in SpecializedQuestModel.path:
            
            SpecializedQuestModel.path[self.level] = {}
            
        # while there are remaining nodes (items)
        while self.rowCount() > 0:
            
            # pop & pick the right most node
            node = self.items[self.rowCount() - 1]
            self.pop(self.rowCount() - 1)
            
            is_selected = node['selected']
            key = node['name']

            # if user does not select this specialization, do nothing
            if not is_selected:

                continue
                        
            assert key in SpecializedQuestModel.reference[self.level], f'Invalid graph structure, key={key} does not exist (2)'
            
            # first store node states
            # e.g., if the user select/unselect a node, it has to be the same whenever user back to this node
            SpecializedQuestModel.items_dictionary[key] = node
                            
            for child in SpecializedQuestModel.reference[self.level][key]:
                
                if child in Config.invalid_specialized_quest:
                    
                    continue
                
                # for (level - 1) store child parent (i.e., level 0 has no parent, that is why [level - 1] is more convenient)
                SpecializedQuestModel.path[self.level][child] = key
                
                children.append(child)
          
        # new items            
        for key in children:
            
            self.append(SpecializedQuestModel.items_dictionary[key])
        
        # update current level
        self.level += 1
    
        self.setState(SpecializedQuestState.Idle)

        # return success indicator
        return 1
    
    @QtCore.pyqtSlot(result=int)
    def previous(self):
        
        self.setState(SpecializedQuestState.Loading)
                    
        # remove all nodes (items)
        self.removeAll()
        
        self.set_specialization_level_at(self.level - 1)

        self.setState(SpecializedQuestState.Idle)

        # return success indicator
        return 1
    
    @QtCore.pyqtSlot(int)
    def set_specialization_level_at(self, level):
        
        """This function makes sure that is possible to start from any given depth (specialization levels)
        """
        
        has_parent = (SpecializedQuestModel.base_level < level)
        has_parent &= ((level - 1) in SpecializedQuestModel.path)
                
        # remove all nodes (items)
        self.removeAll()
        
        # add new items
        for key in SpecializedQuestModel.reference[level]:
            
            if key in Config.invalid_specialized_quest:
            
                continue
            
            if has_parent:
                
                if not (key in SpecializedQuestModel.path[level - 1]):
                    
                    continue
                
                parent = SpecializedQuestModel.path[level - 1][key]
                is_selected = SpecializedQuestModel.items_dictionary[parent]['selected']
                
                if not is_selected:
                    
                    continue
                            
            self.append(SpecializedQuestModel.items_dictionary[key])

        self.level = level
    
    @QtCore.pyqtSlot(result=bool)
    def isAnySelected(self):
        
        state = False
        
        for item in self.items:
            
            state |= item['selected']
        
        return state
    
    @QtCore.pyqtSlot(str, int)
    def set_service_status(self, node_name, status):
        
        for i, item in enumerate(self.items):

            if item['name'] == node_name:
                
                self.updateRole(i, 'status', status)
                break
    
    @QtCore.pyqtSlot()
    def makeRequest(self):
        
        def _is_selected(key):
            
            if key in Config.invalid_specialized_quest:
                
                return True
                
            return SpecializedQuestModel.items_dictionary[key]['selected']
        
        queries = graph_utils.reduce_any(Config.specialized_quest_types, condition_fn=_is_selected, 
                                         has_cycle=False, childs_key='childs')
        
        if len(queries) == len(Config.invalid_specialized_quest):
            
            queries = set(list(SpecializedQuestModel.items_dictionary.keys()))
        
        else:
            
            for key in Config.invalid_specialized_quest:
                
                queries.remove(key)

        self.query_model.reset(profiles_id=tracer.get_models_id(queries))
    