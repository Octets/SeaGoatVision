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

import numpy as np
import scipy.weave.ext_tools as ext_tools
import os
import sys
import time

from SeaGoatVision.server.core.filter import Filter
from cpp_code import *
from python_code import *
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)

BUILD_DIR = 'build'
RELOAD_DIR = os.path.join('build', 'reload')
has_configure = False
has_destroy = False

def import_all_cpp_filter(cppfiles, cpptimestamps, module, file, extra_link_arg=[], extra_compile_arg=[]):
    """
    This method finds and compile every c++ filters
    If a c++ file changed, the file must be recompiled in a new .so file
    """
    # param :
    # module like sys.modules[__name__]
    # file is __file__ from __init__.py
    _create_build(cppfiles)

    dirname = os.path.dirname(file)
    for f in os.listdir(dirname):
        if not f.endswith(".cpp"):
            continue
        filename, _ = os.path.splitext(f)
        cppcode = open(os.path.join(dirname, f)).read()

        code = "cv::Mat execute(cv::Mat "
        if code not in cppcode:
            code += "image)"
            log.print_function(logger.error, "Missing execute function into %s like \"%s\"" % (filename, code))
            continue

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

        mod = _compile_cpp(modname, cppcode, extra_link_arg, extra_compile_arg)

        _create_python_code(mod, filename, cppcode)

        _create_module(cpptimestamps, module, filename, mod)

def _create_build(cppfiles):
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    if not os.path.exists(RELOAD_DIR):
        os.mkdir(RELOAD_DIR)
    if not cppfiles:
        for f in os.listdir(RELOAD_DIR):
            os.remove(os.path.join(RELOAD_DIR, f))

def _create_module(cpptimestamps, module, modname, mod):
    try:
        logger.info("Begin compile %s.", modname)
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
                    'py_init_global_param' : py_init_global_param,
                    'set_original_image' : create_set_original_image(getattr(cppmodule, 'set_original_image_' + modname)),
                    'set_global_params_cpp' : create_set_global_params(getattr(cppmodule, 'set_global_params_' + modname)),
                    '__doc__' : getattr(cppmodule, 'help_' + modname)()
                }
        if has_configure:
            dct_fct['configure'] = create_configure(getattr(cppmodule, 'config_' + modname))
        if has_destroy:
            dct_fct['destroy'] = create_destroy(getattr(cppmodule, 'destroy_' + modname))

        clazz = type(modname,
                     (Filter,),
                     dct_fct)
        clazz.__module_init__ = module
        setattr(module, modname, clazz)
        del clazz
    except Exception as e:
        log.printerror_stacktrace(logger, e)

def _create_python_code(mod, modname, cppcode):
    # param variable size
    p = {}
    pip = py_init_param
    pip_global = py_init_global_param
    py_notify = Filter().notify_output_observers
    image = np.zeros((1, 1), dtype=np.uint8)
    image_original = np.zeros((1, 1), dtype=np.uint8)
    dct_global_param = {}

    # help
    func = ext_tools.ext_function('help_' + modname, help_code(), [])
    mod.add_function(func)

    # __init__
    func = ext_tools.ext_function('init_' + modname, init_code("void init()" in cppcode), ['p', 'pip', 'py_notify', 'dct_global_param', 'pip_global'])
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

    # destroy
    if "void destroy()" in cppcode:
        has_destroy = True
        func = ext_tools.ext_function('destroy_' + modname, destroy_code(), [])
        mod.add_function(func)
    else:
        has_destroy = False

    # set original image
    func = ext_tools.ext_function('set_original_image_' + modname, set_original_image_code(), ['image_original'])
    mod.add_function(func)

    # set global params
    func = ext_tools.ext_function('set_global_params_' + modname, set_global_params_code(), ['dct_global_param'])
    mod.add_function(func)

    # execute
    # Get the size of parameter
    func = ext_tools.ext_function('exec_' + modname, execute_code(), ['image'])
    func.customize.add_support_code(params_code())
    func.customize.add_support_code(cppcode)
    func.customize.add_support_code(notify_code())
    mod.add_function(func)

def _compile_cpp(modname, cppcode, lst_extra_link, lst_extra_compile):
    # Compile filters
    # The included files are found in the .cpp file
    mod = ext_tools.ext_module(modname)

    for line in cppcode.split('\n'):
        if line.startswith('#include'):
            mod.customize.add_header(line.replace('#include ', ''))
    mod.customize.add_header("<Python.h>")
    mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv`")
    for extra_link in lst_extra_link:
        mod.customize.add_extra_link_arg(extra_link)
    for extra_compile in lst_extra_compile:
        mod.customize.add_extra_compile_arg(extra_compile)
    # add debug symbol
    mod.customize.add_extra_compile_arg("-g")
    mod.customize.add_extra_compile_arg("-pipe")

    return mod
