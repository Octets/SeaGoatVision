
class DataExtractor(object):
    def __init__(self):
        self._output_observers = list()
    
    def notify_output_observers(self, data):
        for obs in self._output_observers:
            obs(data)
        
    def add_output_observer(self, observer):
        self._output_observers.append(observer)
        
    def remove_output_observer(self, observer):
        self._output_observers.remove(observer)