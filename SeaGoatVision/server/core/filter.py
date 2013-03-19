from SeaGoatVision.commun.param import Param

class Filter(object):
    def __init__(self):
        self._output_observers = list()

    def configure(self):
        pass

    def get_params(self, param_name=None):
        params = []
        for name in dir(self):
            var = getattr(self, name)
            if not isinstance(var, Param):
                continue
            if param_name:
                if var.get_name() == param_name:
                    return var
            else:
                params.append(var)
        return params

    def notify_output_observers(self, data):
        for obs in self._output_observers:
            obs(data)

    def add_output_observer(self, observer):
        self._output_observers.append(observer)

    def remove_output_observer(self, observer):
        self._output_observers.remove(observer)
