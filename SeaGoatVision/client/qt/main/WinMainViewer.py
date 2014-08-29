
from PySide import QtCore
from PySide import QtGui
from SeaGoatVision.client.qt.utils import get_ui


class WinMainViewer(QtGui.QMainWindow):

    def __init__(self):
        super(WinMainViewer, self).__init__()
        self.ui = get_ui(self)
        self.grid = self.ui.gridLayout
