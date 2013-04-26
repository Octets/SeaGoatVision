/*
 * camera.h
 *
 *  Created on: 2013-02-04
 *      Author: Junior Gregoire
 *      E-mail: junior.gregoire@gmail.com
 */

#ifndef CAMERA_H_
#define CAMERA_H_

#include "PvApi.h"
#include <opencv2/opencv.hpp>

#define PY_UFUNC_UNIQUE_SYMBOL
#define CHANNEL 3

#include "ImageLib.h"
#include <stdio.h>
#include <queue>
#include <exception>
#include <boost/python.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/numeric.hpp>
#include <boost/python/tuple.hpp>
#include <ndarrayobject.h>



using namespace std;
using namespace boost::python;

enum AcquisitionMode {Continuous,SingleFrame,MultiFrame,Recorder};
static const char* acquisitionMode[]={"Continuous","SingleFrame","MultiFrame","Recorder"};

enum PixelFormat {Mono8,Bayer8,Bayer16,Rgb24,Bgr24,Rgba32,Bgra32};

enum ConfigFileIndex {Factory,Index1,Index2,Index3,Index4,Index5};

namespace exposure{
    enum ExposureMode{Manuel,AutoOnce,Auto,External};
    enum ExposureAutoMode{ExposureAutoAdjustTol,ExposureAutoAlg,ExposureAutoMax,ExposureAutoMin,ExposureAutoOutliers,ExposureAutoRate,ExposureAutoTarger};
    enum ExposureAutoAlgMode{Mean,FitRange};
}

namespace gain{
    enum GainMode{Manuel,AutoOnce,Auto};
    enum GainAutoMode{GainAutoAdjustTol,GainAutoMax,GainAutoMin,GainAutoOutliers,GainAutoRate,GainAutoTarget};
}

namespace whitebal{
    enum WhitebalMode{Manuel,Auto,AutoOnce};
    enum WhitebalAutoMode{WhitebalAutoAdjustTol,WhiteAutoRate};
}

class CameraNotInitializeException: public exception
{
    virtual const char* what() const throw()
    {
        return "Camera is not initialize.";
    }
};

class CameraNotStartException: public exception
{
    virtual const char* what() const throw()
    {
        return "Camera is not started.";
    }
};

class Camera
{
public:
    Camera();
    ~Camera();
    void initialize();
    void uninitialize();

    //Command
    void start();
    void stop();
    void abort();
    void loadConfigFile();
    void saveConfigFile();

    //configuration methods
    void setPixelFormat(PixelFormat);
    const char* getPixelFormat();

    void setAcquisitionMode(AcquisitionMode);
    const char* getAcquisitionMode();

    void setConfigFileIndex(ConfigFileIndex);
    const char* getConfigFileIndex();

    int getTotalBytesPerFrame();

    //ROI methods
    int getHeight();
    void setHeight(int);

    int getWidth();
    void setWidth(int);

    int getRegionX();
    void setRegiontX(int);

    int getRegionY();
    void setRegionY(int);

    //Gamma methods
    float getGamma();
    void setGamma(float);

    //Exposure methods
    const char* getExposureMode();
    void setExposureMode(exposure::ExposureMode);
    void setExposureValue(int value);
    int getExposureValue();
    void setExposureAutoMode(exposure::ExposureAutoMode,int);
    const char* getExposureAutoMode();
    void setExposureAutoMode(exposure::ExposureAutoMode, exposure::ExposureAutoAlgMode);
    const char* getExposureAutoAlg();

    //Gain methods
    const char* getGainMode();
    void setGainMode(gain::GainMode);
    void setGainAutoMode(gain::GainAutoMode,int);
    void setGainValue(int);

    //Hue methods
    int getHue();
    void setHue(int);

    //Saturation methods
    int getSaturation();
    void setSaturation(int);

    //WhiteBalance methods
    const char* getWhitebalMode();
    void setWhitebalMode(whitebal::WhitebalMode);
    const char* getWhitebalAutoMode();
    void setWhitebalAutoMode(whitebal::WhitebalAutoMode,int);
    int getWhitebalValueRed();
    void setWhitebalValueRed(int);
    int getWhitebalValueBlue();
    void setWhitebalValueBlue();

    PyObject* getFrame();

private:
    tPvHandle cam;
    tPvFrame frame;
    PyObject* numImg;
    npy_intp dims[CHANNEL];
    int channel;
    char* array;
    CameraNotInitializeException camNotInit;
    CameraNotStartException camNotStart;

    //private methods
    void setChannel(PixelFormat);

};




#endif /* CAMERA_H_ */
