from typing import Dict, Any, Optional

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractListModel, QObject


class ListModel(QAbstractListModel):
    
    def __init__(self, roles, parent: Optional[QObject] = ...) -> None:
        
        super().__init__(parent)
        
        self.roles = roles
        self.items = []
        
    def append(self, item: Dict[str, Any]):
                
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(item)
        self.endInsertRows()
    
    def update(self, index, item):
        
        idx = self.index(index, 0)
        
        self.items[index] = item
        
        self.dataChanged.emit(idx, idx, self.roleNames())
    
    def updateRole(self, index, role, value):
        
        if not (0 <= index < len(self.items)):
            
            return
        
        idx = self.index(index, 0)
        
        self.items[index][role] = value
        
        self.dataChanged.emit(idx, idx, self.roleNames())
        
    def pop(self, index):
        
        self.beginRemoveColumns(QtCore.QModelIndex(), index, index)
        self.items.pop(index)
        self.endRemoveRows()
    
    def removeAll(self):
        
        while self.rowCount() > 0:
            
            self.pop(self.rowCount() - 1)
            
    def rowCount(self, parent=QtCore.QModelIndex()):
        
        return len(self.items)

    def data(self, index, role_index):
        
        key = self.roles[role_index]
        
        return self.items[index.row()][key]
        
    def roleNames(self):
        
        roles = list(map(lambda name: name.encode(), self.roles))
        
        return dict(enumerate(roles))

    @QtCore.pyqtSlot(int, str, result=QtCore.QVariant)
    def getRole(self, index, role):
        
        return self.items[index][role]
