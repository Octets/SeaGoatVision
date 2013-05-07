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

def init_code(call_c_init):
    """
    This method returns the code to initialize the parameters
    """
    code = """
        params = p;
        py_init_param = pip;
        notify_py = py_notify;
    """
    if call_c_init:
        code += """
            init();
        """
    return code

def execute_code():
    """
    Return the code that calls a c++ filter
    """
    return """
        cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
        cv::Mat ret = execute(mat);
        if (mat.data != ret.data)
            image = ret.data;
    """

def params_code():
    """
    Support code to declare parameters in the C++ filters
    It assumes a method py_init_param received as a parameter from
    the python side to create the parameters in the python object.
    """
    return """
        py::dict params;
        py::object py_init_param;
        long param_int(std::string name, int value, int min, int max) {
            if(!params.has_key(name)) {
                py::tuple args(4);
                args[0] = name;
                args[1] = value;
                args[2] = min;
                args[3] = max;
                py_init_param.call(args);
            }
            py::object o = params.get(name);
            return PyInt_AsLong(o.mcall("get"));
        }

        bool param_bool(std::string name, bool value) {
            if(!params.has_key(name)) {
                py::tuple args(2);
                args[0] = name;
                args[1] = PyBool_FromLong(value);
                py_init_param.call(args);
            }
            py::object o = params.get(name);
            return PyInt_AsLong(o.mcall("get"));
        }

        double param_double(std::string name, double value, double min, double max) {
            if(!params.has_key(name)) {
                py::tuple args(4);
                args[0] = name;
                args[1] = value;
                args[2] = min;
                args[3] = max;
                py_init_param.call(args);
            }
            py::object o = params.get(name);
            return PyFloat_AsDouble(o.mcall("get"));
        }
    """

def notify_code():
    """
    Notify send information to output observer.
    """
    return """
        py::object notify_py;
        void notify(const char *format, ...) {
            py::tuple notify_args(1);
            int done;
            char buffer[512];
            va_list args;

            va_start(args, format);
            done = vsnprintf(buffer, 512, format, args);
            va_end(args);
            if (done > 0) {
                notify_args[0] = buffer;
                notify_py.call(notify_args);
            }
        }
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

def config_code():
    """
    Code to reconfigure the filter
    """
    return """
        configure();
    """
