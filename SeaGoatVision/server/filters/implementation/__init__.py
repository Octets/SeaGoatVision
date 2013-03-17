#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This filename is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
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
import time
import traceback
import numpy as np
import scipy.weave.ext_tools as ext_tools

from SeaGoatVision.server.filters.dataextract import DataExtract
import SeaGoatVision.globals as g

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
def compile_cpp_filters():
    """
    This method finds and compile every c++ filters
    If a c++ file changed, the file must be recompiled in a new .so file
    """

    BUILD_DIR = 'build'
    RELOAD_DIR = os.path.join('build', 'reload')
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    if not os.path.exists(RELOAD_DIR):
        os.mkdir(RELOAD_DIR)
    if not len(g.cppfiles):
        for f in os.listdir(RELOAD_DIR):
            os.remove(os.path.join(RELOAD_DIR, f))

    image = np.zeros((1,1), dtype=np.uint8)
    notify = None

    def init():
        def __init__(self):
            self._output_observers = list()
        return __init__

    def ext_code():
        """
        Return the code that calls a c++ filter
        """
        return """
            cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
            cv::Mat ret = execute(mat, notify);
            if (mat.data != ret.data)
                image = ret.data;
            """

    def help_code():
        """
        Return the code that returns the help string from a c++ file
        """
        return """
            #ifdef DOCSTRING
            return_val = DOCSTRING;
            #else
            return_val = "";
            #endif
            """

    def create_execute(cppfunc):
        """
        Create and return an "execute" method for the dynamically
        created class that wraps the c++ filters
        """
        def execute(self, image):
            notify = self.notify_output_observers
            cppfunc(image, notify)
            return image
        return execute

    dirname = os.path.dirname(__file__)
    for f in os.listdir(dirname):
        if not f.endswith(".cpp"):
            continue
        filename, _ = os.path.splitext(f)
        cppcode = open(os.path.join(dirname, f)).read()

        #Verify if there are changes in the c++ code file.  If there are
        #changes, add a timestamp to the filter .so file name to force a
        #reimportation of the new filter.
        if g.cppfiles.has_key(filename):
            if cppcode != g.cppfiles[filename]:
                g.cpptimestamps[filename] = str(int(time.time()))
        g.cppfiles[filename] = cppcode

        if g.cpptimestamps.has_key(filename):
            modname = filename + g.cpptimestamps[filename]
        else:
            modname = filename

        #Compile filters
        #The included files are found in the .cpp file
        mod = ext_tools.ext_module(modname)
        [mod.customize.add_header(line.replace('#include ', ''))
                                 for line in cppcode.split('\n')
                                 if line.startswith('#include')]
        mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv`")

        func = ext_tools.ext_function(filename, ext_code(),['image', 'notify'])
        func.customize.add_support_code(cppcode)
        mod.add_function(func)

        helpfunc = ext_tools.ext_function('help_' + filename, help_code(), [])
        mod.add_function(helpfunc)

        try:
            if g.cpptimestamps.has_key(filename):
            #Reloaded modules are saved in the reload folder for easy cleanup
                mod.compile(RELOAD_DIR)
            else:
                mod.compile(BUILD_DIR)

            cppmodule = __import__(modname)

            clazz = type(filename, (DataExtract,),
                         {'__init__' : init(),
                          'execute' : create_execute(getattr(cppmodule, filename)),
                          '__doc__' : getattr(cppmodule, 'help_' + filename)()})
            setattr(sys.modules[__name__], filename, clazz)
            del clazz
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.stderr.write(traceback.format_exc() + "\n")

compile_cpp_filters()
