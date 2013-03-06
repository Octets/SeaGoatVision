import os
import scipy.weave.ext_tools as ext_tools

cppmodules = []

mod = ext_tools.ext_module('cppfilters')

for f in os.listdir(os.path.dirname(__file__)):
    filename, _ = os.path.splitext(f)
    cppmodules.append(filename)
    cppcode = open(filename).read()

    extcode = """
        cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
        cv::Mat ret = execute(mat);
        if (mat.data != ret.data)
            ret.copyTo(mat);
        """
        
    helpcode = """
        #ifdef DOCSTRING
        help = Py::new_reference_to(Py::String(DOCSTRING));
        #endif    
    """
    cppmod = ext_tools.ext_function(filename, extcode,['image'])
    cppmod.customize.add_support_code(cppcode)

    helpmod = ext_tools.ext_function('help_' + filename, extcode,['help'])
    helpmod.customize.add_support_code(helpcode)
    
    mod.add_function(cppmod)
    mod.add_function(helpmod)
    
mod.compile()    
for module in cppmodules:    
    code = """from %(module)s import *""" % {'module' : filename} 
    exec code
    
class testt:
    
    def __init__(self):
        pass
    