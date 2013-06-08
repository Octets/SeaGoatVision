from PySide import QtCore
from PySide import QtGui
from camera import ExposureAutoMode
from camera import ExposureAutoAlgMode

class ExposureAutoDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self._initCurrentValues()
        self.setupUpUi()
        
        
    def setupUpUi(self):
        #Setup up current values in widgets
        self._initUIValues()
                
        #Setup Widgets with these signal and actions
        self.ui.meanRadioButton.clicked.connect(self.setExposureAutoAlgMean)
        self.ui.fitRangeRadioButton.clicked.connect(self.setExposureAutoAlgFitRange)
        self.ui.exposureAutoAdjustTolSlider.valueChanged.connect(self.setExposureAutoAdjustTol)
        self.ui.exposureAutoMinLineEdit.textEdited.connect(self.setExposureAutoMin)
        self.ui.exposureAutoMaxLineEdit.textEdited.connect(self.setExposureAutoMax)
        self.ui.exposureAutoOutliersSlider.valueChanged.connect(self.setExposureAutoOutliers)
        self.ui.exposureAutoTargetSlider.valueChanged.connect(self.setExposureAutoTarget)
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValues)
    
    def _initUIValues(self):
        self.ui.exposureAutoAdjustTolSlider.setValue(self.exposureAutoAdjustTol)
        self._setupExposureAutoAlgGroup(self.exposureAutoAlg)
        self.ui.exposureAutoMinLineEdit.setText(str(self.exposureAutoMin))
        self.ui.exposureAutoMaxLineEdit.setText(str(self.exposureAutoMax))
        self.ui.exposureAutoRateSlider.setValue(self.exposureAutoRate)
        self.ui.exposureAutoOutliersSlider.setValue(self.exposureAutoOutliers)
        self.ui.exposureAutoTargetSlider.setValue(self.exposureAutoTarget)
        
    def _initCurrentValues(self):
        self.exposureAutoAdjustTol = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol)
        self.exposureAutoAlg = self.cam.getExposureAutoAlgMode()
        self.exposureAutoMin = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoMin)
        self.exposureAutoMax = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoMax)
        self.exposureAutoOutliers = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers)
        self.exposureAutoRate = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoRate)
        self.exposureAutoTarget = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoTarget)
    
    def _setupExposureAutoAlgGroup(self,exposureAutoAlg):
        if exposureAutoAlg == "Mean":
            self.ui.meanRadioButton.setChecked(True)
        else:
            self.ui.fitRangeRadioButton.setChecked(True)
    
    def resetValues(self):
        self._initUIValues()
        self.ui.setVisible(False)
    
    def ok(self):
        self._initCurrentValues()
        self.ui.setVisible(False)
    
    def setExposureAutoAlgMean(self):
        self.setExposureAutoAlg("Mean")
        
    def setExposureAutoAlgFitRange(self):
        self.setExposureAutoAlg("FitRange")
    
    def setExposureAutoAdjustTol(self,value):
        self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol,value)
    
    def setExposureAutoAlg(self,algo):
        if algo == "Mean":
            self.cam.setExposureAutoModeAlg(ExposureAutoAlgMode.Mean)
        else:
            self.cam.setExposureAutoModeAlg(ExposureAutoAlgMode.FitRange)
    
    def setExposureAutoMin(self,min):
        try:
            self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMin,min)
        except RuntimeError as e:
            QtGui.QMessageBox.warning(self.ui,str(e))
    
    def setExposureAutoMax(self,max):
        try:
            self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMax,max)
        except RuntimeError as e:
            QtGui.QMessageBox.warning(self.ui,str(e))
    
    def setExposureAutoOutliers(self,value):
        self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers,value)
    
    def setExposureAutoRate(self,rate):
        self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoRate,rate)
    
    def setExposureAutoTarget(self,value):
        self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoTarget,value)
    
    
    
    