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

#include "ImageLib.h"
#include <stdio.h>
#include <queue>
#include <exception>
#include <boost/python.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/numeric.hpp>
#include <boost/python/tuple.hpp>
#include <ndarrayobject.h>



#define ENTER 13



using namespace std;
using namespace boost::python;

enum AcquisitionMode {Continuous,SingleFrame,MultiFrame,Recorder};

enum PixelFormat {Mono8,Bayer8,Bayer16,Rgb24,Bgr24,Rgba32,Bgra32};

enum ConfigFileIndex {Factory,Index1,Index2,Index3,Index4,Index5};


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

    int getHeight();
    void setHeight(int);

    int getWidth();
    void setWidth(int);

    //int getRegionX();
    //void setRegiontX(int);

    //int getRegionY();
    //void setRegionY(int);

    PyObject* getFrame();

private:
    tPvHandle cam;
    tPvFrame frame;
    npy_intp dims[];
    int channel;
    char* array;
    CameraNotInitializeException camNotInit;
    CameraNotStartException camNotStart;

    //private methods
    void setChannel(PixelFormat);

};




#endif /* CAMERA_H_ */
