import os
import sys
import numpy as np
import scipy.weave.ext_tools as ext_tools

cppmodules = []
image = np.zeros((1,1), dtype=np.uint8)
help = ""

mod = ext_tools.ext_module('cppfilters')
mod.customize.add_header('<opencv2/opencv.hpp>')
mod.customize.add_header('<opencv2/gpu/gpu.hpp>')

mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv`")

dirname = os.path.dirname(__file__)
for f in os.listdir(dirname):
    if not f.endswith(".cpp"):
        continue
    filename, _ = os.path.splitext(f)
    cppmodules.append(filename)
    cppcode = open(os.path.join(dirname, f)).read()

    extcode = """
        cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
        cv::Mat ret = execute(mat);
        if (mat.data != ret.data)
            ret.copyTo(mat);
        """

    func = ext_tools.ext_function(filename, extcode,['image'])
    func.customize.add_support_code(cppcode)
    mod.add_function(func)

    #helpcode = """
    #    #ifdef DOCSTRING
    #    help = "hello!";
    #    #endif
    #"""
    #helpmod = ext_tools.ext_function('help_' + filename, helpcode,['help'])
    #helpmod.customize.add_support_code(cppcode)
    #mod.add_function(helpmod)

try:
    mod.compile()
    def create_execute(cppfunc):
        def execute(self, image):
            cppfunc(image)
            return image
        return execute

    import cppfilters
    from cppfilters import *
    for module in cppmodules:
        #code = """from cppfilters import %(module)s""" % {'module' : module}
        #exec code
        clazz = type(module, (object,),
                     {'execute' : create_execute(globals()[filename]),
                      '__doc__' : "C++ filter"})#getattr(cppfilters, 'help_' + filename)()})
        setattr(sys.modules[__name__], module, clazz)
        del clazz
except Exception as e:
    print(e)
