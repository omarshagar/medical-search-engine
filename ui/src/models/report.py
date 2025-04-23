from typing import Dict, Any

from PyQt5 import QtCore

from ..types.abstract import ListModel

from .output import OutputModel

from ..config import Config

from .. import utils

class ReportStatus:
    
    Archived = -1
    OnProgress = 0
    Active = 1
    
class ReportModel(ListModel):

    num_reports = 0
    current_id = 0
    
    # ================================================================

    repository: Dict[Any, Any] = {}
        
    # ================================================================
    
    anyStatusChanged = QtCore.pyqtSignal(int)
    outputsReady = QtCore.pyqtSignal()
    
    # ================================================================

    def __init__(self, roles, parent=None):
        
        super(ReportModel, self).__init__(roles=roles, parent=parent)

        self.query_model = None
                
    def set_query_model(self, query_model):
        
        self.query_model = query_model
        
    @QtCore.pyqtSlot(str, str)
    def appendReport(self, report_id, query_index):
        
        if report_id in ReportModel.repository:

            return
        
        query_profile = self.query_model.getProfile(query_index)

        report = Config.get_report_item(report_id=report_id, profile_id=query_profile['profile_id'], default=None)
        
        report['status'] = ReportStatus.OnProgress
        report['profile']['inputs_model'] = query_profile['inputs_model'].clone()
        report['profile']['outputs_model'] = None
        
        ReportModel.repository[report_id] = report
        
        self.append(report)
        
        self.anyStatusChanged.emit(-1)
        
    @QtCore.pyqtSlot(int, result=QtCore.QVariant)
    def getOutputsModel(self, index):
        
        return self.items[index]['profile']['outputs_model']
            
    @QtCore.pyqtSlot(int, result=QtCore.QVariant)
    def getReportProfile(self, index):
        
        if index >= len(self.items):
            
            return
        
        return self.items[index]['profile']
        
    @QtCore.pyqtSlot(dict)
    def setOutputs(self, index, outputs): 
        
        print(index, outputs)
                        
        if outputs is None:
            
            self.setStatus(index, ReportStatus.Archived)
        
        else:
            
            profile = self.items[index]['profile']

            outputs_model = OutputModel(roles=None)
            outputs_model.reset(outputs=outputs)
            
            profile['outputs_model'] = outputs_model
            
            self.updateRole(index, 'profile', profile)
            self.setStatus(index, ReportStatus.Active)
        
        # self.outputsReady.emit()

    @QtCore.pyqtSlot(int, result=list)
    def parseHeader(self, index):
        
        header = self.items[index]['header']   
                
        labels = []
        
        labels.append(header['title'])
        
        if self.items[index]['status'] == ReportStatus.OnProgress:
            
            labels.append('On Progress')
            
        deta_time = utils.get_timedelta(header['created_at'], in_seconds=True)
        
        if deta_time < 1:
        
            labels.append('Just Now')
            
            return labels
        
        else:
        
            return self.updateHeader(index)['labels']
            
    
    @QtCore.pyqtSlot(int, result=QtCore.QVariant)
    def updateHeader(self, index):
        
        header = self.items[index]['header']   
        
        delta_string, fixed = utils.timedelta_format(header['created_at'])
                                               
        labels = []
        
        labels.append(header['title'])

        if self.items[index]['status'] == ReportStatus.OnProgress:
            
            labels.append('On Progress')
                    
        if not fixed:
            
            labels.append(delta_string)
            
        else:
            
            labels.extend(utils.local_time_format(header['created_at']))
            
        return {'labels': labels, 'fixed': fixed}
                   
    @QtCore.pyqtSlot(int, int)
    def setStatus(self, index, status):
    
        self.updateRole(index, 'status', status)
        self.anyStatusChanged.emit(index)

    @QtCore.pyqtSlot(str, int)
    def set_service_status(self, node_name, status):
        
        for i, item in enumerate(self.items):
            
            if item['report_id'] == node_name:
                
                self.updateRole(i, 'status', status)
                break

    def next(self):
        
        self.current_id += 1
        
        return self.current_id
