from PySide import QtCore
from PySide import QtGui

class ExposureManualDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self.currentValue = self.cam.getExposureValue()
        
    def setupUpUi(self):
        self.ui.exposureValueLineEdit.setText(str(self.currentValue))
        self.ui.exposureValueLineEdit.textChanged.connect(self.setExposureValue)
        
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.resetValue)
        
    def resetValue(self,value):
        self.ui.exposureValueLineEdit.setText(str(self.currentValue))
        self.ui.setVisible(False)
    
    def setExposureValue(self,value):
        try:
            self.cam.setExposureValue(int(value))
        except RuntimeError as e:
            QtGui.QMessageBox.warning(self.ui,str(e))
    
    def ok(self):
        self.currentValue = self.cam.getExposureValue()
        self.ui.setVisible(False)