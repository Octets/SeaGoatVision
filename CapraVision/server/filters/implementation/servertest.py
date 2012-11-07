
from CapraVision.server.filters.filter import Filter

class ServerTest(Filter):
    """Send a example line"""
    
    def __init__(self):
        Filter.__init__(self)
    
    def execute(self, image):
        self.notify_output_observers("LineOrientation: x1=0 y1=0 x2=100 y2=100 \n")
        self.notify_output_observers("LineOrientation: \n")
        return image