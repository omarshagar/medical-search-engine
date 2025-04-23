import time
from threading import Thread
from typing import List

from PyQt5 import QtCore

from ..types.abstract import ListModel

from .inputs import InputModel

from ..config import Config

from backend import tracer


class Worker(QtCore.QObject):
    
    finished = QtCore.pyqtSignal()
    running = QtCore.pyqtSignal()

    def __init__(self, fn, kwargs, parent=None) -> None:
        
        super().__init__(parent)
        
        self.fn = fn
        self.kwargs = kwargs
        
    def run(self):
        
        self.running.emit()
        
        self.fn(**self.kwargs)
        
        self.finished.emit()
        
class QueryModel(ListModel):
    
    def __init__(self, roles, parent=None):
        
        super(QueryModel, self).__init__(roles=roles, parent=parent)

        self.report_model = None
    
    def set_report_model(self, report_model):
        
        self.report_model = report_model
        
    @QtCore.pyqtSlot(int, result=QtCore.QVariant)
    def getProfile(self, index):
        
        if (index is None) or (index >= len(self.items)):
            
            return

        return self.items[index]['profile']
    
    @QtCore.pyqtSlot(int, int)
    def setStatus(self, index, status):
        
        self.updateRole(index, 'status', status)
    
    @QtCore.pyqtSlot(int)
    def checkAndUpdateSelected(self, index):
                        
        inputs_model: InputModel = self.items[index]['profile']['inputs_model']
        inputs_state = inputs_model.getInputsState()
        
        state = (inputs_state['remaining_count'] == 0) and (inputs_state['all_valid'])
        
        self.updateRole(index, 'selected', state)
    
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
    
    @QtCore.pyqtSlot(str)
    def appendProfile(self, profile_id: str):
                                                
        query = Config.get_query_item(profile_id=profile_id, default=None)
        
        metadata = query['profile']['metadata']
        
        query['profile']['inputs_model'] = InputModel(roles=None)
        query['profile']['inputs_model'].reset(inputs_metadata=metadata['inputs'])
                
        self.append(query)
            
    @QtCore.pyqtSlot(list)
    def reset(self, profiles_id: List[str]):
                        
        self.removeAll()
                        
        for profile_id in profiles_id:
            
            self.appendProfile(profile_id=profile_id)
            
    @QtCore.pyqtSlot()
    def makeRequest(self):
        
        queries = []
        
        for i, item in enumerate(self.items):
            
            if item['selected']:
                
                virt_profile = self.getProfile(i)
                
                model_id = virt_profile['profile_id']
                report_id = self.report_model.next()
                
                queries.append(virt_profile['inputs_model'].toSpecializedQuestGraph(model_id=model_id))
                
                self.report_model.appendReport(report_id=report_id, query_index=i)
        
        def set_outputs(queries):
            
            for query in queries:
                
                outputs = tracer.pipeline.execute_specialized_quest_query(command='predict', inputs=query)

                self.report_model.setOutputs(self.report_model.num_reports, outputs)
                self.report_model.num_reports += 1
            
        self.thread = QtCore.QThread()
        self.worker = Worker(fn=set_outputs, kwargs={'queries': queries})
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.report_model.outputsReady)
        self.thread.start()
