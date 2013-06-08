from PySide import QtCore
from PySide import QtGui

class WhiteBalanceManualDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        
        self._initCurrentValues()
        self.setupUpUi()
        
    def setupUpUi(self):
        self._initUIValues()
        
        self.ui.whitebalRedValueSlider.valueChanged.connect(self.setRedValue)
        self.ui.whitebalBlueValueSlider.valueChanged.connect(self.setBlueValue)
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValues)
    
    def _initUIValues(self):
        self.ui.whitebalRedValueSlider.setValue(self.currentRedValue)
        self.ui.whitebalBlueValueSlider.setValue(self.currentBlueValue)
            
    def _initCurrentValues(self):
        self.currentRedValue = self.cam.getWhitebalValueRed()
        self.currentBlueValue = self.cam.getWhitebalValueBlue()
    
    def ok(self):
        self._initCurrentValues()
        self.ui.setVisible(False)
        
    def resetValues(self):
        self._initUIValues()
        self.ui.setVisible(False)
    
    def setRedValue(self,value):
        self.cam.setWhitebalValueRed(value)
    
    def setBlueValue(self,value):
        self.cam.setWhitebalValueBlue(value)
        