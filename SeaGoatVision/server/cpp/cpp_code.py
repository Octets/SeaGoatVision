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
        global_param = dct_global_param;
        py_init_param = pip;
        py_init_global_param = pip_global;
        notify_py = py_notify;
    """
    if call_c_init:
        code += """
            init();
        """
    return code

def destroy_code():
    """
    call the destructor
    """
    return """
        destroy();
    """

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

def set_original_image_code():
    return """
        cv::Mat mat_original(Nimage_original[0], Nimage_original[1], CV_8UC(3), image_original);
        original_image = mat_original;
    """

def set_global_params_code():
    return """
        global_param = dct_global_param;
    """

def params_code():
    """
    Support code to declare parameters in the C++ filters
    It assumes a method py_init_param received as a parameter from
    the python side to create the parameters in the python object.
    """
    return """
        py::dict global_param;
        py::dict params;
        py::object py_init_param;
        py::object py_init_global_param;
        /*#########################
        #### CLIENT PARAMETER #####
        ###########################*/
        long param_get_int(std::string name) {
            if(!params.has_key(name)) {
                printf("ERROR from cpp_code param_get_int: key %s not exist.\n", name.c_str());
                return 0;
            }
            py::object o = params.get(name);
            return PyInt_AsLong(o.mcall("get"));
        }

        bool param_get_bool(std::string name) {
            if(!params.has_key(name)) {
                printf("ERROR from cpp_code param_get_bool: key %s not exist.\n", name.c_str());
                return 0;
            }
            py::object o = params.get(name);
            return (bool)(PyInt_AsLong(o.mcall("get")) != 0);
        }

        double param_get_double(std::string name) {
            if(!params.has_key(name)) {
                printf("ERROR from cpp_code param_get_double: key %s not exist.\n", name.c_str());
                return 0;
            }
            py::object o = params.get(name);
            return PyFloat_AsDouble(o.mcall("get"));
        }

        std::string param_get_string(std::string name) {
            if(!params.has_key(name)) {
                printf("ERROR from cpp_code param_get_string: key %s not exist.\n", name.c_str());
                return "";
            }
            py::object o = params.get(name);
            char* data = PyString_AsString(o.mcall("get"));
            if (data == NULL) {
                return "";
            }
            return std::string(data);
        }

        long param_int(std::string name, int value, int min, int max) {
            if(!params.has_key(name)) {
                py::tuple args(4);
                args[0] = name;
                args[1] = value;
                args[2] = min;
                args[3] = max;
                py_init_param.call(args);
            }
            return param_get_int(name);
        }

        bool param_bool(std::string name, bool value) {
            if(!params.has_key(name)) {
                py::tuple args(2);
                args[0] = name;
                args[1] = PyBool_FromLong(value);
                py_init_param.call(args);
            }
            return param_get_bool(name);
        }

        std::string param_string(std::string name, std::string value) {
            if(!params.has_key(name)) {
                py::tuple args(2);
                args[0] = name;
                args[1] = value;
                py_init_param.call(args);
            }
            return param_get_string(name);
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
            return param_get_double(name);
        }

        /*#############################
        #####  ORIGINAL IMAGE #########
        ###############################*/
        cv::Mat original_image;
        cv::Mat get_image_original() {
            return original_image;
        }

        /*###########################################
        ##### GLOBAL PARAMETER - INTER FILTER #######
        #############################################*/
        void global_param_set_int(std::string name, int value) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_set_int: key %s not exist.\n", name.c_str());
            }
            py::object o = global_param.get(name);
            py::tuple args(1);
            args[0] = value;
            o.mcall("set", args);
        }

        void global_param_set_bool(std::string name, bool value) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_set_bool: key %s not exist.\n", name.c_str());
            }
            py::object o = global_param.get(name);
            py::tuple args(1);
            args[0] = PyBool_FromLong(value);
            o.mcall("set", args);
        }

        void global_param_set_double(std::string name, double value) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_set_double: key %s not exist.\n", name.c_str());
            }
            py::object o = global_param.get(name);
            py::tuple args(1);
            args[0] = value;
            o.mcall("set", args);
        }

        void global_param_set_string(std::string name, std::string value) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_set_string: key %s not exist.\n", name.c_str());
            }
            py::object o = global_param.get(name);
            py::tuple args(1);
            args[0] = value;
            o.mcall("set", args);
        }

        void global_param_set_mat(std::string name, cv::Mat cvmat) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_set_mat: key %s not exist.\n", name.c_str());
            }
            py::object o = global_param.get(name);

            /* Convert cv::Mat to numpy */
            int nrows = cvmat.rows;
            int ncols = cvmat.cols;
            npy_intp dims[2] = {nrows, ncols};
            PyObject *value = PyArray_SimpleNewFromData(2, dims, NPY_UBYTE, cvmat.data);

            py::tuple args(1);
            args[0] = value;
            o.mcall("set", args);
        }

        long global_param_get_int(std::string name) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_get_int: key %s not exist.\n", name.c_str());
                return 0;
            }
            py::object o = global_param.get(name);
            return PyInt_AsLong(o.mcall("get"));
        }

        bool global_param_get_bool(std::string name) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_get_bool: key %s not exist.\n", name.c_str());
                return false;
            }
            py::object o = global_param.get(name);
            return (bool)(PyInt_AsLong(o.mcall("get")) != 0);
        }

        double global_param_get_double(std::string name) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_get_double: key %s not exist.\n", name.c_str());
                return 0.0;
            }
            py::object o = global_param.get(name);
            return PyFloat_AsDouble(o.mcall("get"));
        }

        std::string global_param_get_string(std::string name) {
            if(!global_param.has_key(name)) {
                printf("ERROR from cpp_code global_param_get_string: key %s not exist.\n", name.c_str());
                return "";
            }
            py::object o = global_param.get(name);
            char* data = PyString_AsString(o.mcall("get"));
            if (data == NULL) {
                return "";
            }
            return std::string(data);
        }

        cv::Mat global_param_get_mat(std::string name) {
            if(!global_param.has_key(name))
                return cv::Mat();
            try {
                py::object o = global_param.get(name);
                o = o.mcall("get");

                PyArrayObject* image_array = convert_to_numpy(o, name.c_str());
                conversion_numpy_check_type(image_array, PyArray_UBYTE, name.c_str());
                npy_intp* Nimage = image_array->dimensions;
                npy_ubyte* image = (npy_ubyte*) image_array->data;

                cv::Mat mat(Nimage[0], Nimage[1], CV_8UC(3), image);
                /* TODO what we increment?
                Py_XDECREF(py_image);
                */
                return mat;
            } catch (const std::string& ex) {
                printf("Error with conversion numpy to cv::Mat : %s\\n", ex.c_str());
            }
            return cv::Mat();
        }

        long global_param_int(std::string name, int value, int min, int max) {
            if(!global_param.has_key(name)) {
                py::tuple args(4);
                args[0] = name;
                args[1] = value;
                args[2] = min;
                args[3] = max;
                py_init_global_param.call(args);
            }
            return global_param_get_int(name);
        }

        double global_param_double(std::string name, double value, double min, double max) {
            if(!global_param.has_key(name)) {
                py::tuple args(4);
                args[0] = name;
                args[1] = value;
                args[2] = min;
                args[3] = max;
                py_init_global_param.call(args);
            }
            return global_param_get_double(name);
        }

        bool global_param_bool(std::string name, bool value) {
            if(!global_param.has_key(name)) {
                py::tuple args(2);
                args[0] = name;
                args[1] = PyBool_FromLong(value);
                py_init_global_param.call(args);
            }
            return global_param_get_bool(name);
        }

        std::string global_param_string(std::string name, std::string value) {
            if(!global_param.has_key(name)) {
                py::tuple args(2);
                args[0] = name;
                args[1] = value;
                py_init_global_param.call(args);
            }
            return global_param_get_string(name);
        }

        cv::Mat global_param_mat(std::string name, cv::Mat cvmat) {
            if(!global_param.has_key(name)) {
                /* Convert cv::Mat to numpy */
                int nrows = cvmat.rows;
                int ncols = cvmat.cols;
                npy_intp dims[2] = {nrows, ncols};
                PyObject *result = PyArray_SimpleNewFromData(2, dims, NPY_UBYTE, cvmat.data);

                py::tuple args(2);
                args[0] = name;
                args[1] = result;
                py_init_global_param.call(args);
            }
            return global_param_get_mat(name);
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
        void notify_str(const std::string message) {
            if(message.empty())
                return;
            py::tuple notify_args(1);
            notify_args[0] = message;
            notify_py.call(notify_args);
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
