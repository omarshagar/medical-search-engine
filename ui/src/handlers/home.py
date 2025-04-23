from PyQt5 import QtCore

class HomePage(QtCore.QObject):
    
    optionSelected = QtCore.pyqtSignal(bool)
    optionId = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        
        super(HomePage, self).__init__(parent)

        self._option_selected = False
        self._option_id = None
    
    @QtCore.pyqtProperty(bool, notify=optionSelected)
    def option_selected(self):
        
        return self._option_selected
    
    @option_selected.setter
    def option_selected(self, state):
        
        if self._option_selected != state:
            
            self._option_selected = state
            self.optionSelected.emit(state)

    @QtCore.pyqtProperty(str, notify=optionId)
    def option_id(self):
        
        return self._option_id
    
    @option_id.setter
    def option_id(self, option):
        
        if self._option_id != option:
            
            self._option_id = option
            self.optionId.emit(option)
