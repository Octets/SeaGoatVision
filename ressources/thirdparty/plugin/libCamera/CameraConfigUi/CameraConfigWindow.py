from camera import Camera
from camera import ConfigFileIndex
from camera import PixelFormat
from camera import ExposureMode
from camera import WhitebalMode
from camera import GainMode
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
        
        #if not self.camera.isInitialized():
        #   self._initializedCam()       
           
        #Create QActionGroups 
        (self.loadGroup,self.loadSignalMapper) = self._setQActionGroup(self.ui.menuLoad_Config_File,ConfigFileIndex)
        (self.saveGroup,self.saveSignalMapper) = self._setQActionGroup(self.ui.menuSaves_Config_File,ConfigFileIndex)
        (self.pixelFormatGroup,self.pixelFormatSignalMapper) =self._setQActionGroup(self.ui.menuPixel_Format,PixelFormat)
        (self.gainModeGroup,self.gainModeSignalMapper) = self._setQActionGroup(self.ui.menuGain_Mode,GainMode)
        #self.gammaGroup,self.gammaSignalMapper = self._setQActionGroup(self.ui.menuGamma)
        (self.exposureGroup,self.exposureSignalMapper) = self._setQActionGroup(self.ui.menuExposure_Mode,ExposureMode)
        (self.whitebalGroup,self.whitebalSignalMapper) = self._setQActionGroup(self.ui.menuWhite_Balance_Mode,WhitebalMode)
        
        #Create Dialogs windows
        self.exposureAutoDialog = ExposureAutoDialog(self.camera,self.getUi("ExposureAutoDialog"))
        self.exposureManualDialog = ExposureManualDialog(self.camera,self.getUi("ExposureManualDialog"))
        self.hueDialog = HueDialog(self.camera,self.getUi("HueDialog"))
        self.roiDialog = ROIDialog(self.camera,self.getUi("ROIDialog"))
        self.saturationDialog = SaturationDialog(self.camera,self.getUi("SaturationDialog"))
        self.whiteBalanceAutoDialog = WhiteBalanceAutoDialog(self.camera,self.getUi("WhiteBalanceAutoDialog"))
        self.whiteBalanceManualDialog = WhiteBalanceManualDialog(self.camera,self.getUi("WhiteBalanceManualDialog"))
        self.gainAutoDialog = GainAutoDialog(self.camera,self.getUi("GainAutoDialog"))
        self.gainManualDialog = GainManualDialog(self.camera,self.getUi("GainManualDialog"))
        
        #Connect Actions
        self.ui.actionStart.triggered.connect(self.start)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionHue.triggered.connect(self.hueDialog.ui.show) 
        self.ui.actionAuto_Gain_Settings.triggered.connect(self.gainManualDialog.ui.show)
        self.ui.actionGain_Value.triggered.connect(self.gainAutoDialog.ui.show)
        self.ui.actionROI.triggered.connect(self.roiDialog.ui.show)
        self.ui.actionAuto_Exposure_Settings.triggered.connect(self.exposureAutoDialog.ui.show)
        self.ui.actionExposure_Value.triggered.connect(self.exposureManualDialog.ui.show)
        self.ui.actionAuto_White_Balance_Settings.triggered.connect(self.whiteBalanceAutoDialog.ui.show)
        self.ui.actionManual_White_Balance_Settings.triggered.connect(self.whiteBalanceManualDialog.ui.show)
        self.ui.actionSaturation.triggered.connect(self.saturationDialog.ui.show)
        
        self._setupUi()
    
    def _setupUi(self):       
     
        self.loadSignalMapper.mapped.connect(self.loadConfigFile) 
        self.saveSignalMapper.mapped.connect(self.savesConfigFile)
        
        self._initUiValues()
        
            
        
    
    def _initUiValues(self):
        self.loadSignalMapper.mapping(self.camera.getConfigFileIndex()).setChecked(True)
        self.saveSignalMapper.mapping(self.camera.getConfigFileIndex()).setChecked(True) 
        self.pixelFormatSignalMapper.mapping(self.camera.getPixelFormat()).setChecked(True)
        self.gainModeSignalMapper.mapping(self.camera.getGainMode()).setChecked(True)
        self.exposureSignalMapper.mapping(self.camera.getExposureMode()).setChecked(True)
        self.whitebalSignalMapper.mapping(self.camera.getWhitebalMode()).setChecked(True)               
             
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
        
            
    def loadConfigFile(self,index):
        self.camera.setConfigFileIndex(index)  
        self.camera.loadConfigFile()
    
    def savesConfigFile(self,index):
        self.camera.setConfigFileIndex(index)
        self.camera.saveConfigFile()      
    
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
            
    def _setQActionGroup(self,menu,enum):
         #Set Menu Saves Config File Chackable
        indexes = menu.actions()
        menu.clear()
        print len(indexes)
        group = QtGui.QActionGroup(self.ui)
        mapper = QtCore.QSignalMapper()  
        group.setExclusive(True)
        
        for item in enum.names.items():
            index = QtGui.QAction(item[0],group)            
            index.setCheckable(True)
            index.triggered.connect(mapper.map)
            mapper.setMapping(index,item[1])            
            group.addAction(index) 
        return group,mapper
    
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
    
        
