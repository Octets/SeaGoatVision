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
#include <boost/algorithm/string.hpp>
#include <ndarrayobject.h>

using namespace std;
using namespace boost::python;
using namespace boost::algorithm;


enum AcquisitionMode {Continuous,SingleFrame,MultiFrame,Recorder,AMCount=Recorder};

enum PixelFormat {Mono8,Bayer8,Bayer16,Rgb24,Bgr24,Rgba32,Bgra32,PFCount=Bgra32};

enum ConfigFileIndex {Factory,Index1,Index2,Index3,Index4,Index5,CFICount=Index5};

namespace exposure{
    enum ExposureMode{Manual,AutoOnce,Auto,External,EMCount=External};
    enum ExposureAutoMode{ExposureAutoAdjustTol,ExposureAutoAlg,ExposureAutoMax,ExposureAutoMin,ExposureAutoOutliers,ExposureAutoRate,ExposureAutoTarget,EAMCount=ExposureAutoTarget};
    enum ExposureAutoAlgMode{Mean,FitRange,EAAMCount=FitRange};
}

namespace gain{
    enum GainMode{Manual,AutoOnce,Auto,GMCount=Auto};
    enum GainAutoMode{GainAutoAdjustTol,GainAutoMax,GainAutoMin,GainAutoOutliers,GainAutoRate,GainAutoTarget,GAMCount=GainAutoTarget};
}

namespace whitebal{
    enum WhitebalMode{Manual,Auto,AutoOnce,WMCount=AutoOnce};
    enum WhitebalAutoMode{WhitebalAutoAdjustTol,WhiteAutoRate,WAMCount=WhiteAutoRate};
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

class StringToEnumConversionException:public exception{
    virtual const char* what() const throw(){
        return "Conversion String to Enum has failed!";
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
    bool isInitialized();
    bool isStarted();

    //Commands
    void start();
    void stop();
    void loadConfigFile();
    void saveConfigFile();

    PyObject* getCam();
    void startVideo();
    void stopVideo();

    //configuration methods
    void setPixelFormat(PixelFormat);
    PixelFormat getPixelFormat();

    void setAcquisitionMode(AcquisitionMode);
    AcquisitionMode getAcquisitionMode();

    void setConfigFileIndex(ConfigFileIndex);
    ConfigFileIndex getConfigFileIndex();

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
    exposure::ExposureMode getExposureMode();
    void setExposureMode(exposure::ExposureMode);
    void setExposureValue(int value);
    int getExposureValue();
    void setExposureAutoMode(exposure::ExposureAutoMode,int);
    exposure::ExposureAutoAlgMode getExposureAutoAlgMode();
    void setExposureAutoAlgMode(exposure::ExposureAutoAlgMode);
    int getExposureAutoMode(exposure::ExposureAutoMode);

    //Gain methods
    gain::GainMode getGainMode();
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
    whitebal::WhitebalMode getWhitebalMode();
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
    bool started;
    bool initialized;
    bool videoStarted;

    //private methods
    void setChannel(PixelFormat);
    void checkIfValueIsAPercent(int);
    void checkIfValueIsAHalfPercent(int);
    bool checkFloatValue(float,float);
    void checkWhitebalValue(int);
    void checkIfCameraIsInitialized();


    template <class E>
    E stringToEnum(string index,const char* stringTable[],int Count){
        trim(index);
        for(int i=0;i<Count;i++)
        {
            if(string(stringTable[i]).compare(index))
            {
                return (E)i;
            }
        }
        throw StringToEnumConversionException();
    }

};




#endif /* CAMERA_H_ */
