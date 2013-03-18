from SeaGoatVision.commun.param import Param
from SeaGoatVision.server.filters.dataextract import DataExtract 

class Filter(DataExtract):
    def __init__(self):
        DataExtract.__init__(self)

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