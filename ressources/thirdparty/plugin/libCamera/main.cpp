/********************************************************************************************
 * main.cpp
 *
 *  Created on: 2013-02-03
 *  Author: Junior Gregoire
 *  E-mail: junior.gregoire@gmail.com
 *
 *  Class Description:
 *      This is the main class for the python shared library for ethernet camera Manta g-095c.
 *      Main class construct a c++ to python interface for Camera class.
 *      I use boost::python framework to make this interface
 **********************************************************************************************/



#include "camera.h"
#include <iostream>
#include <boost/python.hpp>
using namespace boost::python;

/********************************************************************************************
    This is the debut of the definition of python module.
    The builded module have to have the same name as the boost python definition name.
    By example: if you define your module with "BOOST_PYTHON_MODULE(potatoe)", your builded module
    have to be named potatoe.so or potatoe.dll or you will not be able to import your module with
    python.
*********************************************************************************************/
BOOST_PYTHON_MODULE(camera)
{
    //This is necessary to use numpy array
    _import_array();

    //This is the definition of AcquitionMode enum to python camera module
    enum_<AcquisitionMode>("AcquisitionMode")
        .value(acquisitionMode[Continuous],Continuous)
        .value("SingleFrame",SingleFrame)
        .value("MultiFrame",MultiFrame)
        .value("Recorder",Recorder)
    ;

    //This is the definition of PixelFormat enum to python camera module
    enum_<PixelFormat>("PixelFormat")
        .value("Mono8",Mono8)
        .value("Bayer8",Bayer8)
        .value("Bayer16",Bayer16)
        .value("Rgb24",Rgb24)
        .value("Bgr24",Bgr24)
        .value("Rgba32",Rgba32)
        .value("Bgra32",Bgra32)
    ;

    //This is the definition of ConfigFileIndex enum to python camera module
    enum_<ConfigFileIndex>("ConfigFileIndex")
        .value("Factory",Factory)
        .value("Index1",Index1)
        .value("Index2",Index2)
        .value("Index3",Index3)
        .value("Index4",Index4)
        .value("Index5",Index5)
    ;

    /*************************************************************************************
        This is the definition of Camera class to python camera module.
        All methods you want to be visible in your module have to be define here.
    **************************************************************************************/
    class_<Camera>("Camera")
        .def("initialize", &Camera::initialize)
        .def("uninitialize",&Camera::uninitialize)
        .def("start", &Camera::start)
        .def("stop",&Camera::stop)
        .def("getFrame",&Camera::getFrame)
        .def("abort",&Camera::abort)
        .def("loadConfigFile",&Camera::loadConfigFile)
        .def("saveConfigFile",&Camera::saveConfigFile)
        .def("setPixelFormat",&Camera::setPixelFormat)
        .def("getPixelFormat",&Camera::getPixelFormat)
        .def("setAcquisitionMode",&Camera::setAcquisitionMode)
        .def("getAcquisitionMode",&Camera::getAcquisitionMode)
        .def("setConfigFileIndex",&Camera::setConfigFileIndex)
        .def("getConfigFileIndex",&Camera::getConfigFileIndex)
        .def("getTotalBytesPerFrame",&Camera::getTotalBytesPerFrame)
        .def("getHeight",&Camera::getHeight)
        .def("setHeight",&Camera::setHeight)
        .def("getWidth",&Camera::getWidth)
        .def("setWidth",&Camera::setWidth)
    ;
}


