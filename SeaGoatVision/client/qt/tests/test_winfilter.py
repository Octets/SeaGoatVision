

from SeaGoatVision.client.qt.main import WinFilter
from SeaGoatVision.server.filters.implementation import *

class TestWinFilter():
    def test(self):
        filter = blur.Blur()
        self.win = WinFilter(filter)
        self.win.show()