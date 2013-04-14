/************************************************************************************************
 * camera.cpp
 *
 *  Created on: 2013-02-04
 *  Author: Junior Gregoire
 *  E-mail: junior.gregoire@gmail.com
 *
 *  Class Description:
 *      This class have the responsability to make a abstraction of the library PvApi.h
        of Allied Technology. PvApi.h is a library use to communicate to this ethernet camera
        Manta g-095c. This class is used to simplify the definition of c++-python interface.
 *************************************************************************************************/

#include "camera.h"
#include <iostream>

#define CHANNEL 3

//These string arrays exist to simplify convertion of enums to string
static const char* acquisitionMode[]={"Continuous","SingleFrame","MultiFrame","Recorder"};
static const char* pixelFormat[]={"Mono8","Bayer8","Bayer16","Rgb24","Bgr24","Rgba32","Bgra32"};
static const char* configFileIndex[]={"Factory","1","2","3","4","5"};

Camera::Camera()
{
    //This is necessary to use numpy array
    _import_array();

    cam=NULL;
    frame = tPvFrame();
    camNotInit = CameraNotInitializeException();
    camNotStart = CameraNotStartException();

    array = NULL;

}

Camera::~Camera()
{
    this->stop();
    this->uninitialize();
    delete array;
}


void Camera::initialize()
{

    if(PvInitialize()==ePvErrSuccess)
    {
        cout<<"Camera module for Manta G-95c version 0.6"<<endl;
    }
    while(PvCameraCount()==0);

    tPvCameraInfoEx lInfos[1];
    tPvUint32       lCount;

    // list all the cameras currently connected
    PvCameraListEx(lInfos,1,&lCount,sizeof(tPvCameraInfoEx));

    if(lCount == 1)
    {
        std::cout<<"camera found!\n";
        if(lInfos[0].PermittedAccess & ePvAccessMaster)
        {
            tPvUint32 lMaxSize = 8228;
            PvCameraOpen(lInfos[0].UniqueId,ePvAccessMaster,&(this->cam));
            // get the last packet size set on the camera
            PvAttrUint32Get(this->cam,"PacketSize",&lMaxSize);
            // adjust the packet size according to the current network capacity
            PvCaptureAdjustPacketSize(this->cam,lMaxSize);


            this->setPixelFormat(Bgr24);
            //set frame triggers to be generated internally
            PvAttrEnumSet(this->cam, "FrameStartTriggerMode", "Freerun");
            //set camera to receive continuous number of frame    triggers
           this->setAcquisitionMode(Continuous);

            PvCaptureStart(this->cam);
        }
    }
    else
    {
        std::cout<<"camera not found!\n";
    }
}

void Camera::uninitialize(){
    PvCaptureQueueClear(this->cam);
    PvCameraClose(this->cam);
    PvCaptureEnd(this->cam);
    PvUnInitialize();
}

void Camera::start()
{
    if(this->cam == NULL)
    {
        throw camNotInit;
    }

    //start camera receiving frame triggers
    PvCommandRun(this->cam, "AcquisitionStart");
    //unsigned long maxSize;

    int frameSize = getTotalBytesPerFrame();
    int frameWidth =getWidth();
    int frameHeight = getHeight();

    dims[0] = frameHeight;
    dims[1] = frameWidth;
    dims[2] = channel;

    frame.ImageBufferSize = frameSize;

    if(array != NULL){
        delete array;
    }

    array = new char[frameSize];
    //cout << "papaya3" <<endl;
    frame.ImageBuffer=array;

}

void Camera::stop(){
     PvCommandRun(this->cam, "AcquisitionStop");
}

void Camera::abort(){
    PvCommandRun(this->cam,"AcquisitionAbort");
}

void Camera::loadConfigFile(){
    PvCommandRun(this->cam,"ConfigFileLoad");
}

void Camera::saveConfigFile(){
    PvCommandRun(this->cam,"ConfigFileSave");
}

void Camera::setPixelFormat(PixelFormat pf){
    PvAttrEnumSet(this->cam,"PixelFormat",pixelFormat[pf]);
    setChannel(pf);
}

const char* Camera::getPixelFormat(){
    char table[10];
    PvAttrEnumGet(this->cam,"PixelFormat",table,10,NULL);
    string pf(table);
    return pf.c_str();
}

void Camera::setAcquisitionMode(AcquisitionMode am){
    PvAttrEnumSet(this->cam,"AcquisitionMode",acquisitionMode[am]);
}

const char* Camera::getAcquisitionMode(){
    char table[20];
    PvAttrEnumGet(this->cam,"AcquisitionMode",table,20,NULL);
    string am(table);
    return am.c_str();
}

void Camera::setConfigFileIndex(ConfigFileIndex cfi){
     PvAttrEnumSet(this->cam,"ConfigFileIndex",configFileIndex[cfi]);
}

const char* Camera::getConfigFileIndex(){
    char table[10];
    PvAttrEnumGet(this->cam,"ConfigFileIndex",table,10,NULL);
    string cfi(table);
    return cfi.c_str();
}

int Camera::getTotalBytesPerFrame(){
    tPvUint32 frameSize;
    PvAttrUint32Get(this->cam, "TotalBytesPerFrame", &frameSize);
    return frameSize;
}

int Camera::getHeight(){
    tPvUint32 height;
    PvAttrUint32Get(this->cam, "Height", &height);
    return height;
}

void Camera::setHeight(int height){
    PvAttrUint32Set(this->cam,"Height",height);
}

int Camera::getWidth(){
    tPvUint32 width;
    PvAttrUint32Get(this->cam,"Width",&width);
    return width;
}

void Camera::setWidth(int width){
    PvAttrUint32Set(this->cam,"Width",width);
}

PyObject* Camera::getFrame()
{

    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    if(array==NULL)
    {
        throw camNotStart;
    }

    PvCaptureQueueFrame(this->cam, &frame, NULL);

    PvCaptureWaitForFrameDone(this->cam, &frame, PVINFINITE);


    PyObject* numImg = PyArray_SimpleNewFromData(CHANNEL,dims,NPY_UINT8,array);

    return numImg;

}

//private methods
void Camera::setChannel(PixelFormat pf){
    switch(pf){
        case Mono8:
        case Bayer8:
        case Bayer16:
            channel = 1;
            break;
        case Bgr24:
        case Rgb24:
            channel = 3;
            break;
        case Bgra32:
        case Rgba32:
            channel = 4;
            break;
        default:
            channel = 0;
    }
}





