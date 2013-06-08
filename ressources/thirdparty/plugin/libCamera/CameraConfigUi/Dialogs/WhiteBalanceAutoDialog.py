from PySide import QtCore
from PySide import QtGui

from camera import WhitebalAutoMode

class WhiteBalanceAutoDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self._initCurrentValues()
        self.setupUpUi()
        
    def setupUpUi(self):
        self._initUIValues()
        
        self.ui.whitebalAutoAdjustTolSlider.valueChanged.connect(self.setWhitebalAutoAdjustTol)
        self.ui.whitebalAutoRateSlider.valueChanged.connect(self.setWhitebalAutoRate) 
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValues)  
    
    def _initUIValues(self):
        self.ui.whitebalAutoAdjustTolSlider.setValue(self.whitebalAutoAdjustTol)
        self.ui.whitebalAutoRateSlider.setValue(self.whitebalAutoRate)
    
    def _initCurrentValues(self):
        self.whitebalAutoAdjustTol = self.cam.getWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol)
        self.whitebalAutoRate = self.cam.getWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate)
        
    def resetValues(self):
        self._initUIValues()
        self.ui.setVisible(False)
    
    def ok(self):
        self._initCurrentValues()
        self.ui.setVisible(False)
    
    def setWhitebalAutoAdjustTol(self,adjustTol):
        self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol,adjustTol)
        
    def setWhitebalAutoRate(self,rate):
        self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate,rate)