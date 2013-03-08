import os
import sys
import traceback
import numpy as np
import scipy.weave.ext_tools as ext_tools

image = np.zeros((1,1), dtype=np.uint8)

extcode = """
    cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
    cv::Mat ret = execute(mat);
    if (mat.data != ret.data)
        ret.copyTo(mat);
    """

helpcode = """
    #ifdef DOCSTRING
    return_val = DOCSTRING;
    #else
    return_val = "";
    #endif
"""

dirname = os.path.dirname(__file__)
for f in os.listdir(dirname):
    if not f.endswith(".cpp"):
        continue
    filename, _ = os.path.splitext(f)
    cppcode = open(os.path.join(dirname, f)).read()

    mod = ext_tools.ext_module(filename)
    [mod.customize.add_header(line.replace('#include ', '')) 
                             for line in cppcode.split('\n') 
                             if line.startswith('#include')]
    mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv`")

    func = ext_tools.ext_function(filename, extcode,['image'])
    func.customize.add_support_code(cppcode)
    mod.add_function(func)

    helpfunc = ext_tools.ext_function('help_' + filename, helpcode, [])
    mod.add_function(helpfunc)

    try:
        mod.compile()
        def create_execute(cppfunc):
            def execute(self, image):
                cppfunc(image)
                return image
            return execute

        def create_help(cppfunc):
            def help(self):
                cpp
        cppmodule = __import__(filename)
        clazz = type(filename, (object,),
                     {'execute' : create_execute(getattr(cppmodule, filename)),
                      '__doc__' : getattr(cppmodule, 'help_' + filename)()})
        setattr(sys.modules[__name__], filename, clazz)
        del clazz
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(traceback.format_exc() + "\n")
                         