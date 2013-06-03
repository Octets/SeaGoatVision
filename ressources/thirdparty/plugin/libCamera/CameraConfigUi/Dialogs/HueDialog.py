from PySide import QtCore
from PySide import QtGui

class HueDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self.hue = self.cam.getHue()
        self.setupUpUi()
        
    def setupUpUi(self):
        self.ui.hueSlider.setValue(self.hue)
        self.ui.hueSlider.valueChanged.connect(self.setHue)
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValue)
        
    def resetValue(self):
        self.ui.hueSlider.setValue(self.hue)
        self.ui.setVisible(False)
        
    def ok(self):
        self.hue = self.cam.getHue()
        self.ui.setVisible(False)        
        
    def setHue(self,value):
        self.cam.setHue(value)
        
    