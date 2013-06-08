from camera import Camera
from PySide import QtUiTools
from PySide import QtCore
from PySide import QtGui

from Dialogs import *

import sys


import __main__

class CameraConfigWindow:
    def __init__(self,camera=None):
        
        self.ui = self.getUi("CameraConfigWindow")  
        
        if camera is None:
            self.camera = Camera()
        
        if not self.camera.isInitialized():
           self._initializedCam()       
           
        #Create QActionGroups 
        self.loadGroup = self._setQActionGroup(self.ui.menuLoad_Config_File)
        self.saveGroup = self._setQActionGroup(self.ui.menuSaves_Config_File)
        self.pixelFormatGroup =self._setQActionGroup(self.ui.menuPixel_Format)
        self.gainModeGroup = self._setQActionGroup(self.ui.menuGain_Mode)
        self.gammaGroup = self._setQActionGroup(self.ui.menuGamma)
        self.exposureGroup = self._setQActionGroup(self.ui.menuExposure_Mode)
        self.whitebalGroup = self._setQActionGroup(self.ui.menuWhite_Balance_Mode)
        
        #Create Dialogs windows
        self.exposureAutoDialog = ExposureAutoDialog(self.camera,self.getUi("ExposureDialog"))
        self.exposureValueDialog = ExposureManualDialog(self.camera,self.getUi("ExposureValueDialog"))
        self.hueDialog = HueDialog(self.camera,self.getUi("HueDialog"))
        self.roiDialog = ROIDialog(self.camera,self.getUi("ROIDialog"))
        self.saturationDialog = SaturationDialog(self.camera,self.getUi("SaturationDialog"))
        self.whiteBalanceDialog = WhiteBalanceDialog(self.camera,self.getUi("WhiteBalanceDialog"))
        self.whiteBalanceManualDialog = WhiteBalanceDialog(self.camera,self.getUi("WhiteBalanceManualDialog"))
        self.gainValueDialog = GainValueDialog(self.camera,self.getUi("GainValueDialog"))
        self.gainDialog = GainValueDialog(self.camera,self.getUi("GainDialog"))
        
        #Connect Actions
        self.ui.actionStart.triggered.connect(self.start)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionHue.triggered.connect(self.hueDialog.ui.show) 
        self.ui.actionAuto_Gain_Settings.triggered.connect(self.gainDialog.ui.show)
        self.ui.actionGain_Value.triggered.connect(self.gainValueDialog.ui.show)
        self.ui.actionROI.triggered.connect(self.roiDialog.ui.show)
        self.ui.actionAuto_Exposure_Settings.triggered.connect(self.exposureAutoDialog.ui.show)
        self.ui.actionExposure_Value.triggered.connect(self.exposureValueDialog.ui.show)
        self.ui.actionAuto_White_Balance_Settings.triggered.connect(self.whiteBalanceDialog.ui.show)
        self.ui.actionManual_White_Balance_Settings.triggered.connect(self.whiteBalanceManualDialog.ui.show)
        self.ui.actionSaturation.triggered.connect(self.saturationDialog.ui.show)
             
    def getUi(self, className):
        loader = QtUiTools.QUiLoader()
        uiPath = str.format("./UiForms/{0}.ui",className)
        print uiPath
        uiFile = QtCore.QFile(uiPath)
        uiFile.open(QtCore.QFile.ReadOnly)
        return loader.load(uiFile)
    
    def start(self):
        self._initializedCam()
        self.camera.start()  
       
        
    def stop(self):
        self.camera.stop()
        self.camera.uninitialize() 
        
            
    def loadConfigFile(self):
        self.camera.getConfigFileIndex()        
    
    def savesConfigFile(self):
        self.camera.getConfigFileIndex()        
    
    def setPixelFormet(self):
        self.camera.getPixelFormat()
    
    def setGainMode(self):
        self.camera.setGainMode()
    
    def setGamma(self):
        self.camera.getGamma()
    
    def setExposureMode(self):
        self.camera.getExposureMode()
    
    def setWhiteBalanceMode(self):
        self.camera.getWhitebalMode()
            
    def _setQActionGroup(self,menu):
         #Set Menu Saves Config File Chackable
        indexes = menu.actions()
        print len(indexes)
        group = QtGui.QActionGroup(self.ui)  
        for index in indexes:
            index.setCheckable(True)
            group.addAction(index) 
    
    def _initializedCam(self):
        if self.camera.isInitialized():
            return
        try:
            self.camera.initialize()
        except RuntimeError as e:
            print e
            QtGui.QMessageBox.warning(self.ui,"Warning",str(e))
          
                     
        
    
if __name__ == "__main__":
    qApplication = QtGui.QApplication(sys.argv);    
    cam = CameraConfigWindow()
    cam.ui.show()
    qApplication.exec_()
    
        
