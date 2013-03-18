"""
Parameter is used by filter and client. This is public variable with specific
type of filter.
Filter must not modify Param.
Different type :
 - INT : integer. Can have min or max value. Can use table of specific value.
 - FLOAT : float. Same of INT, but use float.
 - BOOL : boolean. Only True or False.

TIPS :
 - You want only EVEN number for your gaussian blur?
    lst_gauss_value = [i for i in range(100) if not(i % 2)]
    kern_gauss_blur = Param("kern_gauss_blur", 4, lst_value=lst_gauss_value)
 - In this example, we can't access to -1 because of min.
    p = Param("f", 2, min_v=1, max_v=19, lst_value=[-1,2,4,6,10])
 - We can use a threshold value. In this situation, we have two value.
  The value is always the low value and the threshold_hight is the hight value.
    p = Param("f", 2, min_v=1, max_v=8, thres_h=5)
"""
class Param(object):
    """Param autodetect basic type
    force_type need to be a <type>
    If you want specific type, cast it to basic type and use force_type
    Param manager type : bool, str, int and float
    """
    def __init__(self, name, value, min_v=None, max_v=None, lst_value=None,\
                force_type=None, thres_h=None):
        if type(name) is not str:
            raise Exception("Name must be string value.")
        self.name = name
        self.min_v = None
        self.max_v = None
        self.value = None
        self.default_value = None
        self.type_t = None
        self.thres_h = None
        self.force_type = None
        self._valid_param(value, min_v, max_v, lst_value, thres_h)
        self.set(value)
        self.default_value = self.value
        if force_type:
            self.force_type = force_type
        else:
            self.force_type = self.type_t

    def _valid_param(self, value, min_v, max_v, lst_value, thres_h):
        type_t = type(value)
        if not(type_t is int or type_t is bool or type_t is float or type_t is str):
            raise Exception("Param don't manage type %s" % type_t)
        if type_t is float or type_t is int:
            # check min and max
            if min_v is not None and \
                not(type(min_v) is float or type(min_v) is int):
                raise Exception("min_v must be float or int.")
            if max_v is not None and \
                    not(type(max_v) is float or type(max_v) is int):
                raise Exception("max_v must be float or int.")
            if lst_value is not None and \
                    not(type(lst_value) is tuple or type(lst_value) is list):
                raise Exception("lst_value must be list or tuple")
            if type_t is float:
                min_v = None if min_v is None else float(min_v)
                max_v = None if max_v is None else float(max_v)
                lst_value = None if lst_value is None else \
                            [float(value) for value in lst_value]
            if type_t is int:
                min_v = None if min_v is None else int(min_v)
                max_v = None if max_v is None else int(max_v)
                lst_value = None if lst_value is None else \
                            [int(value) for value in lst_value]
        self.min_v = min_v
        self.max_v = max_v
        self.lst_value = lst_value
        self.type_t = type_t
        self.thres_h = thres_h

    def reset(self):
        self.value = self.default_value

    def get_name(self):
        return self.name

    def get_min(self):
        return self.min_v

    def get_max(self):
        return self.max_v

    def get(self):
        if self.thres_h is not None:
            return (self.force_type(self.value), self.force_type(self.thres_h))
        return self.force_type(self.value)

    def set(self, value, thres_h=None):
        #exception for bool
        if self.type_t is bool:
            value = bool(value)
        if type(value) is not self.type_t:
            raise Exception("value is wrong type. Expected %s and receive %s" \
                    % (self.type_t, type(value)))
        if self.type_t is int or self.type_t is float:
            if self.min_v is not None and value < self.min_v:
                raise Exception("Value %s is lower then min %s" % \
                    (value, self.min_v))
            if self.max_v is not None and value > self.max_v:
                raise Exception("Value %s is upper then max %s" % \
                    (value, self.max_v))
            if self.lst_value is not None and value not in self.lst_value:
                raise Exception("value %s is not in lst of value" % (value))
        if self.thres_h is not None:
            if thres_h is None:
                if value > self.thres_h:
                    msg = "Threshold bot %s is upper then threshold top %s." \
                           % (value, self.thres_h)
                    raise Exception(msg)
            else:
                if type(thres_h) is not self.type_t:
                    msg = "value is wrong type. Expected %s and receive %s" \
                        % (self.type_t, type(value))
                    raise Exception(msg)
                elif value > thres_h:
                    msg = "Threshold low %s is upper then threshold hight %s." \
                           % (value, thres_h)
                    raise Exception(msg)
                if thres_h > self.max_v:
                    raise Exception("Threshold hight %s is upper then max %s." \
                            % (thres_h, self.max_v))
                self.thres_h = thres_h
        self.value = value

    def get_type(self):
        return self.force_type