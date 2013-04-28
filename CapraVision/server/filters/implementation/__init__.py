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
import time
import traceback
import numpy as np
import scipy.weave.ext_tools as ext_tools

import CapraVision.globals as g
from CapraVision.server.filters.parameter import  Parameter

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

def capsule_template():
    return weave.inline(
    """
    Prout p = Prout();
    return_val = PyCapsule_New(&p, "Prout", NULL);    
    """, support_code = "class Prout{};")

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
    if len(g.cppfiles) == 0:
        for f in os.listdir(RELOAD_DIR):
            os.remove(os.path.join(RELOAD_DIR, f))

    image = np.zeros((1,1), dtype=np.uint8)
    params = {}
    capsule = capsule_template()
    
    def ext_code(class_name):
        """
        Return the code that calls a c++ filter
        """
        return """
            class_name* p = static_cast<class_name*> (PyCapsule_GetPointer(capsule, "class_name"));
            p->setInitParam(py_init_param);
            std::cout << "debut" << std::endl;
            p->setParams(params);
            p->init();
            cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
            cv::Mat ret = p->execute(mat);
            if (mat.data != ret.data) {
                ret.copyTo(mat);
            }

            """.replace("class_name", class_name)
    
    def init_code(class_name):
        """
        This method returns the code to initialize the parameters
        """
        return """
            {class_name} p;
            p.setParams(params);
            p.setInitParam(py_init_param);
            p.init();
            return_val = PyCapsule_New(&p, "{class_name}", NULL);            
        """.replace("{class_name}", class_name)
        
    def params_code():
        """
        Support code to declare parameters in the C++ filters
        It assumes a method py_init_param received as a parameter from
        the python side to create the parameters in the python object.
        """
        return """
            class Filter {
                private:
                    py::dict* params;
                    py::object py_init_param;

                    void init_param(char* name, int min, int max, int def_val) {
                            py::tuple args(4);
                            args[0] = name;
                            args[1] = min;
                            args[2] = max;
                            args[3] = def_val;
                            py_init_param.call(args);            
                    } 
                protected:
                    
                    long ParameterAsInt(char* name, int min, int max, int def_val) {
                        std::cout << "paramasint" << std::endl;
                        std::cout << name << std::endl;
                        if(!params->has_key(name)) {
                        std::cout << "hoho" << std::endl;
                            init_param(name, min, max, def_val);
                        }
                        py::object o = params->get(name);
                        o.mcall("get_current_value");
                        int z = o.mcall("get_current_value");
                        std::cout << PyInt_AsLong(o.mcall("get_current_value")) << std::endl;
                        return PyInt_AsLong(o.mcall("get_current_value"));
                    }
                    
                    bool ParameterAsBool(char* name, int min, int max, int def_val) {
                        if(!params->has_key(name)) {
                            init_param(name, min, max, def_val);
                        }
                        return PyInt_AsLong(params->get(name).mcall("get_current_value"));
                    }
                public:
                    void setParams(py::dict p) {
                        params = &p;
                    }
                    void setInitParam(py::object o) {
                        py_init_param = o;
                    }         
            };
            
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
    
    def config_code(class_name):
        """
        """
        return """
            class_name* p = static_cast<class_name*> (PyCapsule_GetPointer(capsule, "class_name"));
            p->setParams(params);
            p->setInitParam(py_init_param);        
            p->configure();
        """.replace("class_name", class_name)
    
    def create_execute(cppfunc):
        """
        Create and return an "execute" method for the dynamically
        created class that wraps the c++ filters
        """
        def execute(self, image):
            cppfunc(image, self.params, self.py_init_param, self.cppclass)
            import cv2
            cv2.imwrite("/home/capra/cpp.png", image)
            return image
        return execute
        
    def create_configure(cppfunc):
        """
        """
        def configure(self):
            cppfunc(self.params, self.py_init_param, self.cppclass)
        return configure
    
    def create_init(cppfunc, params):
        """
        """
        def __init__(self):
            self.cppclass = cppfunc(self.params, self.py_init_param)
        return __init__
    
    def py_init_param(self, name, min, max, def_val):
        param = Parameter(name, min, max, def_val)
        self.params[name] = param
        setattr(self, name, param)
        
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
        #cppcode = cppcode.replace('ParameterAsInt(', 'ParameterAsInt(params, py_init_param, ')
        #cppcode = cppcode.replace('ParameterAsBool(', 'ParameterAsBool(params, py_init_param, ')
        
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
        mod.customize.add_header("<Python.h>")
        mod.customize.add_extra_link_arg("`pkg-config --cflags --libs opencv python`")
    
        func = ext_tools.ext_function('exec_' + filename, ext_code(filename),['image', 'params', 'py_init_param', 'capsule'])
        func.customize.add_support_code(params_code())
        func.customize.add_support_code(cppcode)
        mod.add_function(func)
    
        helpfunc = ext_tools.ext_function('help_' + filename, help_code(), [])
        mod.add_function(helpfunc)
    
        initfunc = ext_tools.ext_function('init_' + filename, init_code(filename), ['params', 'py_init_param'])
        initfunc.customize.add_support_code(params_code())
        initfunc.customize.add_support_code(cppcode)
        mod.add_function(initfunc)
        
        configfunc = ext_tools.ext_function('config_' + filename, config_code(filename), ['params', 'py_init_param', 'capsule'])
        configfunc.customize.add_support_code(params_code())
        configfunc.customize.add_support_code(cppcode)
        mod.add_function(configfunc)
        
        try:
            if g.cpptimestamps.has_key(filename):
            #Reloaded modules are saved in the reload folder for easy cleanup
                mod.compile(RELOAD_DIR)
            else:
                mod.compile(BUILD_DIR)
    
            cppmodule = __import__(modname)
            
            params = {}
            clazz = type(filename, (object,),
                 {'__init__' : create_init(
                                    getattr(cppmodule, 'init_' + filename), params),
                  'configure' : create_configure(
                                    getattr(cppmodule, 'config_' + filename)),
                  'execute' : create_execute(
                                    getattr(cppmodule, 'exec_' + filename)),
                  'py_init_param' : py_init_param, 
                  '__doc__' : getattr(cppmodule, 'help_' + filename)(), 
                  'params' : params})
            
            setattr(sys.modules[__name__], filename, clazz)
            del clazz
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.stderr.write(traceback.format_exc() + "\n")

compile_cpp_filters()