from PySide import QtCore
from PySide import QtGui
from camera import GainAutoMode

class GainAutoDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self._initCurrentValues()
        
    def setupUpUi(self): 
        #Setup up values in widgets
        self._initUIValues()
        
        #Connect widgets signals to 
        self.ui.gainAutoAdjustTolSlider.valueChanged.connect(self.setGainAutoAdjustTol)
        self.ui.gainAutoMaxSlider.valueChanged.connect(self.setGainAutoMax)
        self.ui.gainAutoMinSlider.valueChanged.connect(self.setGainAutoMin)
        self.ui.gainAutoRateSlider.valueChanged.connect(self.setGainAutoRate)
        self.ui.gainAutoOutliersSlider.valueChanged.connect(self.setGainAutoOutliers)
        self.ui.gainAutoRateSlider.valueChanged.connect(self.gainAutoTarget)
           
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValue)
    
    def _initUIValues(self):
        self.ui.gainAutoAdjustTolSlider.setValue(self.gainAutoAdjustTol)
        self.ui.gainAutoMaxSlider.setValue(self.gainAutoMax)
        self.ui.gainAutoMinSlider.setValue(self.gainAutoMin)
        self.ui.gainAutoRateSlider.setValue(self.gainAutoRate)
        self.ui.gainAutoOutliersSlider.setValue(self.gainAutoOutliers)
        self.ui.gainAutoRateSlider.setValue(self.gainAutoTarget)
        
    def _initCurrentValues(self):
        self.gainAutoAdjustTol = self.cam.getGainAutoMode(GainAutoMode.GainAutoAdjustTol)
        self.gainAutoMax = self.cam.getGainAutoMode(GainAutoMode.GainAutoMax)
        self.gainAutoMin = self.cam.getGainAutoMode(GainAutoMode.GainAutoMin)
        self.gainAutoRate = self.cam.getGainAutoMode(GainAutoMode.GainAutoRate)
        self.gainAutoOutliers = self.cam.getGainAutoMode(GainAutoMode.GainAutoOutliers)
        self.gainAutoTarget = self.cam.getGainAutoMode(GainAutoMode.GainAutoTarget)
        
    def resetValue(self,value):
        self._initUIValues()
        self.ui.setVisible(False)   
    
    def ok(self):
        self._initCurrentValues()
        self.ui.setVisible(False)
        
    def setGainAutoAdjustTol(self,adjustTol):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoAdjustTol,adjustTol)
    
    def setGainAutoMax(self,max):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoMax,max)
    
    def setGainAutoMin(self,min):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoMin,min)
    
    def setGainAutoRate(self,rate):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoRate,rate)
    
    def setGainAutoOutliers(self,outliers):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoOutliers,outliers)
    
    def setGainAutoTarget(self,target):
        self.cam.setGainAutoMode(GainAutoMode.GainAutoTarget,target)