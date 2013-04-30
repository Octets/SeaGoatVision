#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
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

import traceback
import numpy as np
import scipy.weave.ext_tools as ext_tools
import os
import sys

from SeaGoatVision.server.core.filter import Filter
from SeaGoatVision.commun.param import Param
from cpp_code import *
from python_code import *

BUILD_DIR = 'build'
RELOAD_DIR = os.path.join('build', 'reload')

def import_all_cpp_filter(cppfiles, cpptimestamps, module, file):
    """
    This method finds and compile every c++ filters
    If a c++ file changed, the file must be recompiled in a new .so file
    """
    # param :
    # module like sys.modules[__name__]
    # file is __file__ from __init__.py
    create_build(cppfiles)

    dirname = os.path.dirname(file)
    for f in os.listdir(dirname):
        if not f.endswith(".cpp"):
            continue
        filename, _ = os.path.splitext(f)
        cppcode = open(os.path.join(dirname, f)).read()

        # Verify if there are changes in the c++ code file.  If there are
        # changes, add a timestamp to the filter .so file name to force a
        # reimportation of the new filter.
        if cppfiles.has_key(filename):
            if cppcode != cppfiles[filename]:
                cpptimestamps[filename] = str(int(time.time()))
        cppfiles[filename] = cppcode

        if cpptimestamps.has_key(filename):
            modname = filename + cpptimestamps[filename]
        else:
            modname = filename

        compile_cpp(cppfiles, cpptimestamps, module, modname, cppcode)

def create_build(cppfiles):
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    if not os.path.exists(RELOAD_DIR):
        os.mkdir(RELOAD_DIR)
    if not cppfiles:
        for f in os.listdir(RELOAD_DIR):
            os.remove(os.path.join(RELOAD_DIR, f))

def compile_cpp(cppfiles, cpptimestamps, module, modname, cppcode):
    def py_init_param(self, name, min, max, def_val):
        param = Param(name, def_val, min_v=min, max_v=max)
        self.params[name] = param
        setattr(self, name, param)

    code = "cv::Mat execute(cv::Mat "
    if code not in cppcode:
        code += "image)"
        print("Error - Missing execute function into %s like \"%s\"" % (modname, code))
        return

    # Compile filters
    # The included files are found in the .cpp file
    mod = ext_tools.ext_module(modname)
    [mod.customize.add_header(line.replace('#include ', ''))
                             for line in cppcode.split('\n')
                             if line.startswith('#include')]
    mod.customize.add_header("<Python.h>")
    mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv`")

    # help
    func = ext_tools.ext_function('help_' + modname, help_code(), [])
    mod.add_function(func)

    # __init__
    # Get the size of parameter
    p = {}
    pip = py_init_param
    py_notify = Filter().notify_output_observers

    func = ext_tools.ext_function('init_' + modname, init_code("void init()" in cppcode), ['p', 'pip', 'py_notify'])
    func.customize.add_support_code(params_code())
    func.customize.add_support_code(notify_code())
    mod.add_function(func)

    # configure
    if "void configure()" in cppcode:
        has_configure = True
        func = ext_tools.ext_function('config_' + modname, config_code(), [])
        func.customize.add_support_code(params_code())
        func.customize.add_support_code(cppcode)
        func.customize.add_support_code(notify_code())
        mod.add_function(func)
    else:
        has_configure = False

    # execute
    # Get the size of parameter
    image = np.zeros((1, 1), dtype=np.uint8)

    func = ext_tools.ext_function('exec_' + modname, ext_code(), ['image'])
    func.customize.add_support_code(params_code())
    func.customize.add_support_code(cppcode)
    func.customize.add_support_code(notify_code())
    mod.add_function(func)

    try:
        if cpptimestamps.has_key(modname):
            # Reloaded modules are saved in the reload folder for easy cleanup
            mod.compile(RELOAD_DIR)
        else:
            mod.compile(BUILD_DIR)

        cppmodule = __import__(modname)
        params = {}
        dct_fct = {'__init__' : create_init(getattr(cppmodule, 'init_' + modname), params),
                    'execute' : create_execute(getattr(cppmodule, 'exec_' + modname)),
                    'py_init_param' : py_init_param,
                    '__doc__' : getattr(cppmodule, 'help_' + modname)()
                }
        if has_configure:
            dct_fct['configure'] = create_configure(getattr(cppmodule, 'config_' + modname))

        clazz = type(modname,
                     (Filter,),
                     dct_fct)
        setattr(module, modname, clazz)
        del clazz
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(traceback.format_exc() + "\n")
