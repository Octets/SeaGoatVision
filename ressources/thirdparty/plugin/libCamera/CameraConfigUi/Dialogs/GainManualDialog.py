from PySide import QtCore
from PySide import QtGui

class GainManualDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self.currentGainValue = self.cam.getGainValue()
        self.setupUpUi()
        
    def setupUpUi(self):
        self.ui.gainValueSlider.setValue(self.currentGainValue)
        self.ui.gainValueSlider.valueChanged.connect(self.setGainValue)
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValue)
    
    def resetValue(self):
        self.ui.gainValueSlider.setNum(self.currentGainValue)
        self.ui.setVisible(False)
        
    def ok(self):
        self.currentGainValue = self.cam.getGainValue()
        self.ui.setVisible(False)
        
    def setGainValue(self,value):
        self.cam.setGainValue(value)