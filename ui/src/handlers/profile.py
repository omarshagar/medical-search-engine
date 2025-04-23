from PyQt5 import QtCore

class Profile(QtCore.QObject):
    
    onPressed = QtCore.pyqtSignal(bool)
    onHovered = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        
        super(Profile, self).__init__(parent)

        self._pressed = False
        self._hovered = False
    
    @QtCore.pyqtProperty(bool, notify=onPressed)
    def pressed(self):
        
        return self._pressed
    
    @pressed.setter
    def pressed(self, state):
        
        if self._pressed != state:
            
            self._pressed = state
            self.onPressed.emit(state)
    
    @QtCore.pyqtProperty(bool, notify=onHovered)
    def hovered(self):
        
        return self._hovered
    
    @hovered.setter
    def hovered(self, state):
        
        if self._hovered != state:
            
            self._hovered = state
            self.onHovered.emit(state)
