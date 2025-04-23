from PyQt5 import QtCore

class Screen(QtCore.QObject):
    
    def __init__(self, parent=None):
        
        super(Screen, self).__init__(parent)

        # target device screen = primary_screen
        self._primary_screen = {'width': 1920, 'height': 1080, 'dpi': 96} 
        self._ref_screen = {'width': 1800, 'height': 900, 'refDpi': 96}
    
    @QtCore.pyqtSlot(float, float)
    def setSize(self, width, height):
        
        self._ref_screen['width'] = width
        self._ref_screen['height'] = height
            
    @QtCore.pyqtSlot(result=float)
    def ratio(self):
        
        width = min(self._primary_screen['width'], self._primary_screen['height'])
        height = max(self._primary_screen['width'], self._primary_screen['height'])
        
        ratio = min(width / self._ref_screen['width'], height / self._ref_screen['height'])
        
        return ratio

    @QtCore.pyqtSlot(result=float)
    def dpi_ratio(self):
        
        dpi = self._primary_screen['dpi']

        width = min(self._primary_screen['width'], self._primary_screen['height'])
        height = max(self._primary_screen['width'], self._primary_screen['height'])
        
        h_ratio = (height * self._ref_screen['refDpi']) / (self._ref_screen['height'] * dpi)
        w_ratio = (width * self._ref_screen['refDpi']) / (self._ref_screen['width'] * dpi)
        
        ratio = min(w_ratio, h_ratio)
        
        return ratio
    
    @QtCore.pyqtSlot(QtCore.QVariant, result=float)
    def rescale(self, size):
        
        return self.ratio() * size
    
    @QtCore.pyqtSlot(QtCore.QVariant, result=float)
    def fontRescale(self, size):
        
        return self.dpi_ratio() * size
    
    @QtCore.pyqtSlot(QtCore.QVariant, result=float)
    def rescaleInverse(self, size):
        
        return (1.0 / self.ratio()) * size
    