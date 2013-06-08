from PySide import QtCore
from PySide import QtGui

class SaturationDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self.saturation = self.cam.getSaturation()
        self.setupUpUi()
        
    def setupUpUi(self):
        self.ui.saturationSpinBox.setValue(self.saturation)
        
        self.ui.saturationSpinBox.valueChanged.connect(self.setSaturation)
        
        
    def resetValue(self):
        self.ui.saturationSpinBox.setValue(self.saturation)
        self.ui.setVisible(False)
        
    def ok(self):
        self.saturation = self.cam.getSaturation()
        self.ui.setVisible(False)
        
    def setSaturation(self,value):
        pass