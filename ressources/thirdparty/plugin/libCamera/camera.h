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

#define PY_UFUNC_UNIQUE_SYMBOL
#define CHANNEL 3
#define MAX_TIMEOUT 5

#include "PvApi.h"
#include <opencv2/opencv.hpp>
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

enum PixelFormat {Mono8,Bayer8,Bayer16,Rgb24,Bgr24,Rgba32,Bgra32};

enum ConfigFileIndex {Factory,Index1,Index2,Index3,Index4,Index5};

namespace exposure{
    enum ExposureMode{Manual,AutoOnce,Auto,External};
    enum ExposureAutoMode{ExposureAutoAdjustTol,ExposureAutoAlg,ExposureAutoMax,ExposureAutoMin,ExposureAutoOutliers,ExposureAutoRate,ExposureAutoTarget};
    enum ExposureAutoAlgMode{Mean,FitRange};
}

namespace gain{
    enum GainMode{Manual,AutoOnce,Auto};
    enum GainAutoMode{GainAutoAdjustTol,GainAutoMax,GainAutoMin,GainAutoOutliers,GainAutoRate,GainAutoTarget};
}

namespace whitebal{
    enum WhitebalMode{Manual,Auto,AutoOnce};
    enum WhitebalAutoMode{WhitebalAutoAdjustTol,WhiteAutoRate};
}

static const char* acquisitionMode[]={"Continuous","SingleFrame","MultiFrame","Recorder"};
static const char* pixelFormat[]={"Mono8","Bayer8","Bayer16","Rgb24","Bgr24","Rgba32","Bgra32"};
static const char* configFileIndex[]={"Factory","1","2","3","4","5"};
static const char* exposureMode[]={"Manual","AutoOnce","Auto","External"};
static const char* exposureAutoMode[]={"ExposureAutoAdjustTol","ExposureAutoAlg","ExposureAutoMax","ExposureAutoMin","ExposureAutoOutliers","ExposureAutoRate","ExposureAutoTarget"};
static const char* exposureAutoAlgMode[]={"Mean","FitRange"};
static const char* gainMode[]={"Manual","AutoOnce","Auto"};
static const char* gainAutoMode[]={"GainAutoAdjustTol","GainAutoMax","GainAutoMin","GainAutoOutliers","GainAutoRate","GainAutoTarget"};
static const char* whitebalMode[]={"Manual","Auto","AutoOnce"};
static const char* whiteAutoMode[]={"WhitebalAutoAdjustTol","WhitebalAutoRate"};

/** Declarations of Exceptions**/
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

class ExposureAutoAlgException:public exception{
    virtual const char* what() const throw(){
        return "For setting or getting value of ExposureAutoAlg, you should use (get | set)ExposureAutoAlgMode";
    }
};

class ExposureValueException:public exception{
     virtual const char* what() const throw(){
        return "ExposureValue is only for Manual Mode.";
    }
};

class ExposureAutoOutliersException:public exception{
     virtual const char* what() const throw(){
        return "Each unit of ExposureAutoOutliers represent 0.01%, so value have to be between 0 and 10 000.";
    }
};

class ExposureMinValueException:public exception{
     virtual const char* what() const throw(){
        return "Manta G-095c have a minimum exposure time of 45 micro-secondes";
    }
};

class GainValueException:public exception{
     virtual const char* what() const throw(){
        return "GainValue is only for Manual Mode.";
    }
};

class GainOutOfRangeException:public exception{
    virtual const char* what() const throw(){
        return "GainValue should be between 0 and 32.";
    }
};

class SaturationOutOfRangeException:public exception{
    virtual const char* what() const throw(){
        return "Saturation value have to be between 0.0 and 2.0";
    }

};

class GammaOutOfRangeException:public exception{
    virtual const char* what() const throw(){
        return "Gamma can have only three values 0.45, 0.5, 0.7 and 1.0 (Disable gamma correction)";
    }
};

class FullPercentValueException:public exception{
    virtual const char* what() const throw(){
        return "This value is a percentage and have to be between 0 and 100";
    }
};

class HalfPercentValueException:public exception{
    virtual const char* what() const throw(){
        return "This value is a percentage and have to be between 0 and 50";
    }
};

class HueOutOfRangeException:public exception{
    virtual const char* what() const throw(){
        return "Hue value should be between -40° to 40°";
    }
};

class WhitebalModeException:public exception{
     virtual const char* what() const throw(){
        return "This white balance value is only for Manual Mode.";
    }
};

class WhitebalValueException:public exception{
     virtual const char* what() const throw(){
        return "This white balance value has to be between 80 to 300.";
    }
};
/** End Declaration of Exception **/
/** CAMERA_h **/
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
    const char* getExposureAutoAlgMode();
    void setExposureAutoAlgMode(exposure::ExposureAutoAlgMode);
    int getExposureAutoMode(exposure::ExposureAutoMode);

    //Gain methods
    const char* getGainMode();
    void setGainMode(gain::GainMode);
    int getGainAutoMode(gain::GainAutoMode);
    void setGainAutoMode(gain::GainAutoMode,int);
    void setGainValue(int);
    int getGainValue();

    //Hue methods
    float getHue();
    void setHue(float);

    //Saturation methods
    float getSaturation();
    void setSaturation(float);

    //WhiteBalance methods
    const char* getWhitebalMode();
    void setWhitebalMode(whitebal::WhitebalMode);
    int getWhitebalAutoMode(whitebal::WhitebalAutoMode);
    void setWhitebalAutoMode(whitebal::WhitebalAutoMode,int);
    int getWhitebalValueRed();
    void setWhitebalValueRed(int);
    int getWhitebalValueBlue();
    void setWhitebalValueBlue(int);

    //Stats methods

private:
    tPvHandle cam;
    tPvFrame frame;
    npy_intp dims[CHANNEL];
    int channel;
    char* array;

    //private methods
    void setChannel(PixelFormat);
    void checkIfValueIsAPercent(int);
    void checkIfValueIsAHalfPercent(int);
    bool checkFloatValue(float,float);
    void checkWhitebalValue(int);
    void checkIfCameraIsInitialized();

};




#endif /* CAMERA_H_ */
