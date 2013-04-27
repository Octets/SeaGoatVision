/*******************************************************
 * camera.h
 *
 *  Created on: 2013-02-04
 *  Author: Junior Gregoire
 *  E-mail: junior.gregoire@gmail.com
 *  Class Description:
 *      This class have the responsability to make a abstraction of the library PvApi.h
 *      of Allied Technology. PvApi.h is a library use to communicate to this ethernet camera
 *      Manta g-095c. This class is used to simplify the definition of c++-python interface.
 *******************************************************/

#ifndef CAMERA_H_
#define CAMERA_H_

#include "PvApi.h"
#include <opencv2/opencv.hpp>

#define PY_UFUNC_UNIQUE_SYMBOL
#define CHANNEL 3
#define MAX_TIMEOUT 5

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
    enum ExposureMode{Manual,AutoOnce,Auto,External};
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

static const char* pixelFormat[]={"Mono8","Bayer8","Bayer16","Rgb24","Bgr24","Rgba32","Bgra32"};
static const char* configFileIndex[]={"Factory","1","2","3","4","5"};
static const char* exposureMode[]={"Manual","AutoOnce","Auto","External"};
//static const char* exposureAutoMode[]={"ExposureAutoAdjustTol","ExposureAutoAlg","ExposureAutoMax","ExposureAutoMin","ExposureAutoOutliers","ExposureAutoRate","ExposureAutoTarger"};
//static const char* exposureAutoAlgMode[]={"Mean","FitRange"};
//static const char* gainMode[]={"Manuel","AutoOnce","Auto"};
//static const char* gainAutoMode[]={"GainAutoAdjustTol","GainAutoMax","GainAutoMin","GainAutoOutliers","GainAutoRate","GainAutoTarget"};
//static const char* whitebalMode[]={"Manuel","Auto","AutoOnce"};
//static const char* whiteAutoMode[]={"WhitebalAutoAdjustTol","WhiteAutoRate"};

class CameraNotInitializeException: public exception
{
    virtual const char* what() const throw()
    {
        return "Camera is not initialized.";
    }
};

class CameraNotStartException: public exception
{
    virtual const char* what() const throw()
    {
        return "Camera is not started.";
    }
};

class PvApiNotInitializeException: public exception
{
    virtual const char* what() const throw(){
        return "PvApi is not initialized.";
    }
};

class Camera
{
public:
    Camera();
    ~Camera();
    void initialize();
    void uninitialize();
    PyObject* getFrame();

    //Commands
    void start();
    void stop();
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
    void setExposureAutoMode(exposure::ExposureAutoMode, exposure::ExposureAutoAlgMode);
    const char* getExposureAutoMode();

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




private:
    tPvHandle cam;
    tPvFrame frame;
    npy_intp dims[CHANNEL];
    int channel;
    char* array;
    CameraNotInitializeException camNotInit;
    CameraNotStartException camNotStart;
    PvApiNotInitializeException pvApiNotInit;

    //private methods
    void setChannel(PixelFormat);

};




#endif /* CAMERA_H_ */
