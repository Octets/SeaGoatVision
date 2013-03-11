

class Parameter:
    INT,FLOAT,EVEN,ODD = range(4)
    
    def __init__(self, name, minValue, maxValue, currentValue, type_t=INT):
        self.name = name
        self.minValue = minValue
        self.maxValue = maxValue
        self.currentValue = currentValue
        self.type = type_t
    
    def get_name(self):
        return self.name
    
    def get_min_value(self):
        return self.minValue
    
    def get_max_value(self):
        return self.maxValue
    
    def get_current_value(self):
        return self.currentValue
    
    def set_current_value(self,newValue):
        self.currentValue = newValue
    
    def get_type(self):
        return self.type