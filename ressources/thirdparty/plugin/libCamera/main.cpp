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
        .value(acquisitionMode[SingleFrame],SingleFrame)
        .value(acquisitionMode[MultiFrame],MultiFrame)
        .value(acquisitionMode[Recorder],Recorder)
    ;

    //This is the definition of PixelFormat enum to python camera module
    enum_<PixelFormat>("PixelFormat")
        .value(pixelFormat[Mono8],Mono8)
        .value(pixelFormat[Bayer8],Bayer8)
        .value(pixelFormat[Bayer16],Bayer16)
        .value(pixelFormat[Rgb24],Rgb24)
        .value(pixelFormat[Bgr24],Bgr24)
        .value(pixelFormat[Rgba32],Rgba32)
        .value(pixelFormat[Bgra32],Bgra32)
    ;

    //This is the definition of ConfigFileIndex enum to python camera module
    enum_<ConfigFileIndex>("ConfigFileIndex")
        .value(configFileIndex[Factory],Factory)
        .value("Index1",Index1)
        .value("Index2",Index2)
        .value("Index3",Index3)
        .value("Index4",Index4)
        .value("Index5",Index5)
    ;

    enum_<exposure::ExposureMode>("ExposureMode")
        .value(exposureMode[exposure::Manual],exposure::Manual)
        .value(exposureMode[exposure::AutoOnce],exposure::AutoOnce)
        .value(exposureMode[exposure::Auto],exposure::Auto)
        .value(exposureMode[exposure::External],exposure::External)
    ;

    enum_<exposure::ExposureAutoMode>("ExposureAutoMode")
        .value(exposureAutoMode[exposure::ExposureAutoAdjustTol],exposure::ExposureAutoAdjustTol)
        .value(exposureAutoMode[exposure::ExposureAutoAlg],exposure::ExposureAutoAlg)
        .value(exposureAutoMode[exposure::ExposureAutoMax],exposure::ExposureAutoMax)
        .value(exposureAutoMode[exposure::ExposureAutoMin],exposure::ExposureAutoMin)
        .value(exposureAutoMode[exposure::ExposureAutoOutliers],exposure::ExposureAutoOutliers)
        .value(exposureAutoMode[exposure::ExposureAutoRate],exposure::ExposureAutoRate)
        .value(exposureAutoMode[exposure::ExposureAutoTarget],exposure::ExposureAutoTarget)
    ;

    enum_<exposure::ExposureAutoAlgMode>("ExposureAutoAlgMode")
        .value(exposureAutoAlgMode[exposure::FitRange],exposure::FitRange)
        .value(exposureAutoAlgMode[exposure::Mean],exposure::Mean)
    ;

    enum_<gain::GainMode>("GainMode")
        .value(gainMode[gain::Manual],gain::Manual)
        .value(gainMode[gain::Auto],gain::Auto)
        .value(gainMode[gain::AutoOnce],gain::AutoOnce)
    ;

    enum_<gain::GainAutoMode>("GainAutoMode")
        .value(gainAutoMode[gain::GainAutoAdjustTol],gain::GainAutoAdjustTol)
        .value(gainAutoMode[gain::GainAutoMax],gain::GainAutoMin)
        .value(gainAutoMode[gain::GainAutoMin],gain::GainAutoMin)
        .value(gainAutoMode[gain::GainAutoOutliers],gain::GainAutoOutliers)
        .value(gainAutoMode[gain::GainAutoRate],gain::GainAutoRate)
        .value(gainAutoMode[gain::GainAutoTarget],gain::GainAutoTarget)
    ;

    enum_<whitebal::WhitebalMode>("WhitebalMode")
        .value(whitebalMode[whitebal::Manual],whitebal::Manual)
        .value(whitebalMode[whitebal::Auto],whitebal::Auto)
        .value(whitebalMode[whitebal::AutoOnce],whitebal::AutoOnce)
    ;

    enum_<whitebal::WhitebalAutoMode>("WhitebalAutoMode")
        .value(whiteAutoMode[whitebal::WhiteAutoRate],whitebal::WhiteAutoRate)
        .value(whiteAutoMode[whitebal::WhitebalAutoAdjustTol],whitebal::WhitebalAutoAdjustTol)
    ;

    /*************************************************************************************
        This is the definition of Camera class to python camera module.
        All methods you want to be visible in your module have to be define here.
    **************************************************************************************/
    class_<Camera>("Camera")
        .def("initialize", &Camera::initialize)
        .def("uninitialize",&Camera::uninitialize)
        .def("getFrame",&Camera::getFrame)

        /**Commands**/
        .def("start", &Camera::start)
        .def("stop",&Camera::stop)

        .def("loadConfigFile",&Camera::loadConfigFile)
        .def("saveConfigFile",&Camera::saveConfigFile)

        /**Condifurations methods**/
        .def("setPixelFormat",&Camera::setPixelFormat)
        .def("getPixelFormat",&Camera::getPixelFormat)
        .def("setAcquisitionMode",&Camera::setAcquisitionMode)
        .def("getAcquisitionMode",&Camera::getAcquisitionMode)
        .def("setConfigFileIndex",&Camera::setConfigFileIndex)
        .def("getConfigFileIndex",&Camera::getConfigFileIndex)
        .def("getTotalBytesPerFrame",&Camera::getTotalBytesPerFrame)

        /**ROI methods**/
        .def("getHeight",&Camera::getHeight)
        .def("setHeight",&Camera::setHeight)
        .def("getWidth",&Camera::getWidth)
        .def("setWidth",&Camera::setWidth)
        .def("getRegionX",&Camera::getRegionX)
        .def("setRegionX",&Camera::setRegiontX)
        .def("getRegionY",&Camera::getRegionY)
        .def("setRegionY",&Camera::setRegionY)

        /** Gamma Methods **/
        .def("getGamma",&Camera::getGamma)
        .def("setGamma", &Camera::setGamma)

        /** Exposure Methods **/
        .def("getExposureMode",&Camera::getExposureMode)
        .def("setExposureMode",&Camera::setExposureMode)
        .def("setExposureValue",&Camera::setExposureValue)
        .def("getExposureValue",&Camera::getExposureValue)
        .def("getExposureAutoMode",&Camera::getExposureAutoMode)
        .def("setExposureAutoMode",&Camera::setExposureAutoMode)
        .def("setExposureAutoAlgMode",&Camera::setExposureAutoAlgMode)
        .def("getExposureAutoAlgMode",&Camera::getExposureAutoAlgMode)

        /** Gain Methods **/
        .def("getGainMode",&Camera::getGainMode)
        .def("setGainMode",&Camera::setGainMode)
        .def("getGainAutoMode",&Camera::getGainAutoMode)
        .def("setGainAutoMode",&Camera::setGainAutoMode)
        .def("setGainValue",&Camera::setGainValue)
        .def("getGainValue",&Camera::getGainValue)

        /** Hue Methods**/
        .def("getHue",&Camera::getHue)
        .def("setHue",&Camera::setHue)

        /** Saturation Methods **/
        .def("getSaturation",&Camera::getSaturation)
        .def("setSaturation",&Camera::setSaturation)

        /** WhiteBalance Methods **/
        .def("getWhitebalMode",&Camera::getWhitebalMode)
        .def("setWhitebalMode",&Camera::setWhitebalMode)
        .def("getWhitebalAutoMode",&Camera::getWhitebalAutoMode)
        .def("setWhitebalAutoMode", &Camera::setWhitebalAutoMode)
        .def("getWhitebalValueRed",&Camera::getWhitebalValueRed)
        .def("setWhitebalValueRed",&Camera::setWhitebalValueRed)
        .def("getWhitebalValueBlue",&Camera::getWhitebalValueBlue)
        .def("setWhitebalValueBlue",&Camera::setWhitebalValueBlue)
    ;
}


