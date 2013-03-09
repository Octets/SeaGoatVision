#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of CapraVision.
#    
#    CapraVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" Filters implementations
    Rules:
        - Filter must be a class
        - Filter must have a execute(image) function that 
            returns the processed image
        - Filter can have a configure() function to configure the 
            object after creation
        - If there are data members that must not be saved, the member name
            must start with an underscore.  
            Eg: self._dont_save = 123 # value will not be save
                self.save = 456 # value will be saved"""

import os
import sys
import traceback
import numpy as np
import scipy.weave.ext_tools as ext_tools

##
# PYTHON FILTERS IMPORT
##
for f in os.listdir(os.path.dirname(__file__)):
    if not f.endswith(".py"):
        continue
    filename, _ = os.path.splitext(f)
    code = 'from %(module)s import *' % {'module' : filename} 
    exec code


##
# C++ FILTERS IMPORT
##
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

        cppmodule = __import__(filename)
        clazz = type(filename, (object,),
                     {'execute' : create_execute(getattr(cppmodule, filename)),
                      '__doc__' : getattr(cppmodule, 'help_' + filename)()})
        setattr(sys.modules[__name__], filename, clazz)
        del clazz
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(traceback.format_exc() + "\n")
