from PySide import QtCore
from PySide import QtGui

class ROIDialog:
    def __init__(self,cam,ui):
        self.cam = cam
        self.ui = ui
        self._initCurrentValues()
        self.setupUpUi()
        
    def setupUpUi(self):
        self._initUiValues()
        
        self.ui.widthLineEdit.textChanged.connect(self.setHeight)
        self.ui.heightLineEdit.textChanged.connect(self.setWidth)
        self.ui.xLineEdit.textChanged.connect(self.setX)
        self.ui.yLineEdit.textChanged.connect(self.setY)
    
    def _initUiValues(self):
        self.ui.widthLineEdit.setText(str(self.width))
        self.ui.heightLineEdit.setText(str(self.height))
        self.ui.xLineEdit.setText(str(self.x))
        self.ui.yLineEdit.setText(str(self.y))
    
    def _initCurrentValues(self):
        self.width = self.cam.getWidth()
        self.height = self.cam.getHeight()
        self.x = self.cam.getRegionX()
        self.y = self.cam.getRegionY()
    
        
    def resetValues(self):
        self._initUiValues()
        self.ui.setVisible(False)
    
    def ok(self):
        self._initCurrentValues()
        self.ui.setVisible(False)
        
    def setWidth(self,value):
        self.cam.setWidth(int(value))
    
    def setHeight(self,value):
        self.cam.setHeight(int(value))
    
    def setX(self,value):
        self.cam.setRegionX(int(value))
    
    def setY(self,value):
        pself.cam.setRegionY(int(value))
        