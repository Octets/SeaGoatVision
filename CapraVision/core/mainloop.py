
import threading
import time

class ThreadMainLoop(threading.Thread):
    """Main thread to process the images.
    
    Args:
        source: the source to receive images from.
        filterchain: the configured filterchain
        sleep_time: time to wait in seconds before getting the next image
    """
    def __init__(self, source, sleep_time):
        threading.Thread.__init__(self)
        self.daemon = True
        self.source = source
        self.sleep_time = sleep_time
        self.running = False
        self.observers = []
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def run(self):
        self.running = True
        for image in self.source:
            if image is None:
                time.sleep(self.sleep_time)
                continue
            self.notify_observers(image)
            if not self.running:
                break
            if self.sleep_time >= 0:
                time.sleep(self.sleep_time)
        self.running = False
        
    def notify_observers(self, image):
        for observer in self.observers:
            observer(image)
            
    def stop(self):
        self.running = False
