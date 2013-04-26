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

#define MAX_TIMEOUT 5

//These string arrays exist to simplify convertion of enums to string

static const char* pixelFormat[]={"Mono8","Bayer8","Bayer16","Rgb24","Bgr24","Rgba32","Bgra32"};
static const char* configFileIndex[]={"Factory","1","2","3","4","5"};
static const char* exposureMode[]={"Manuel","AutoOnce","Auto","External"};
//static const char* exposureAutoMode[]={"ExposureAutoAdjustTol","ExposureAutoAlg","ExposureAutoMax","ExposureAutoMin","ExposureAutoOutliers","ExposureAutoRate","ExposureAutoTarger"};
//static const char* exposureAutoAlgMode[]={"Mean","FitRange"};
//static const char* gainMode[]={"Manuel","AutoOnce","Auto"};
//static const char* gainAutoMode[]={"GainAutoAdjustTol","GainAutoMax","GainAutoMin","GainAutoOutliers","GainAutoRate","GainAutoTarget"};
//static const char* whitebalMode[]={"Manuel","Auto","AutoOnce"};
//static const char* whiteAutoMode[]={"WhitebalAutoAdjustTol","WhiteAutoRate"};

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
    if(array!=NULL){
         this->stop();
         delete array;
    }
    if(cam!=NULL){
       this->uninitialize();
    }


}


void Camera::initialize()
{


    if(PvInitialize()==ePvErrSuccess)
    {
        cout<<"Camera module for Manta G-95c version 0.8"<<endl;
    }

    time_t initTimer = time(NULL);
    time_t currentTimer = time(NULL);
    double seconds = 0;


    while(PvCameraCount()==0 && seconds<MAX_TIMEOUT){
        currentTimer = time(NULL);
        seconds = difftime(currentTimer,initTimer);
    }

    if(seconds>=MAX_TIMEOUT){
        throw camNotInit;
    }

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
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
     PvCommandRun(this->cam, "AcquisitionStop");
}

void Camera::abort(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvCommandRun(this->cam,"AcquisitionAbort");
}

void Camera::loadConfigFile(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvCommandRun(this->cam,"ConfigFileLoad");
}

void Camera::saveConfigFile(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvCommandRun(this->cam,"ConfigFileSave");
}

void Camera::setPixelFormat(PixelFormat pf){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrEnumSet(this->cam,"PixelFormat",pixelFormat[pf]);
    setChannel(pf);
}

const char* Camera::getPixelFormat(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    char table[10];
    PvAttrEnumGet(this->cam,"PixelFormat",table,10,NULL);
    string pf(table);
    return pf.c_str();
}

void Camera::setAcquisitionMode(AcquisitionMode am){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrEnumSet(this->cam,"AcquisitionMode",acquisitionMode[am]);
}

const char* Camera::getAcquisitionMode(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    char table[20];
    PvAttrEnumGet(this->cam,"AcquisitionMode",table,20,NULL);
    string am(table);
    return am.c_str();
}

void Camera::setConfigFileIndex(ConfigFileIndex cfi){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
     PvAttrEnumSet(this->cam,"ConfigFileIndex",configFileIndex[cfi]);
}

const char* Camera::getConfigFileIndex(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    char table[10];
    PvAttrEnumGet(this->cam,"ConfigFileIndex",table,10,NULL);
    string cfi(table);
    return cfi.c_str();
}

int Camera::getTotalBytesPerFrame(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvUint32 frameSize;
    PvAttrUint32Get(this->cam, "TotalBytesPerFrame", &frameSize);
    return frameSize;
}

/** ROI methods**/

int Camera::getHeight(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvUint32 height;
    PvAttrUint32Get(this->cam, "Height", &height);
    return height;
}

void Camera::setHeight(int height){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrUint32Set(this->cam,"Height",height);
}

int Camera::getWidth(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvUint32 width;
    PvAttrUint32Get(this->cam,"Width",&width);
    return width;
}

void Camera::setWidth(int width){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrUint32Set(this->cam,"Width",width);
}

int Camera::getRegionX(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvUint32 regionX;
    PvAttrUint32Get(this->cam,"RegionX",&regionX);
    return regionX;
}

void Camera::setRegiontX(int regionX){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrUint32Set(this->cam,"RegionX",regionX);
}

int Camera::getRegionY(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvUint32 regionY;
    PvAttrUint32Get(this->cam,"RegionY",&regionY);
    return regionY;
}

void Camera::setRegionY(int regionY){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrUint32Set(this->cam,"RegionY",regionY);
}

/** Gamma methods **/
float Camera::getGamma(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    tPvFloat32 gamma;
    PvAttrFloat32Get(this->cam,"Gamma",&gamma);
    return gamma;
}

void Camera::setGamma(float gamma){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrFloat32Set(this->cam,"Gamma",gamma);
}

/** Exposure methods **/
const char* Camera::getExposureMode(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    char table[20];
    PvAttrEnumGet(this->cam,"ExposureMode",table,10,NULL);
    string em(table);
    return em.c_str();
}

void Camera::setExposureMode(exposure::ExposureMode em){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    PvAttrEnumSet(this->cam,"ExposureMode",exposureMode[em]);
}

int Camera::getExposureValue(){
    if(this->cam == NULL)
    {
        throw camNotInit;
    }
    return 0;
}

void Camera::setExposureAutoMode(exposure::ExposureAutoMode eam,int value){

}

const char* Camera::getExposureAutoMode(){
    return NULL;
}

void Camera::setExposureAutoMode(exposure::ExposureAutoMode eam, exposure::ExposureAutoAlgMode eaa){
}

const char* Camera::getExposureAutoAlg(){
    return NULL;
}

/** Gain methods **/
const char* Camera::getGainMode(){
    return NULL;
}

void Camera::setGainMode(gain::GainMode gm){
}

void Camera::setGainAutoMode(gain::GainAutoMode,int){
}
void Camera::setGainValue(int){
}

/** Hue methods **/
int Camera::getHue(){
    return 0;
}

void Camera::setHue(int hue){
}

/** Saturation methods **/
int Camera::getSaturation(){
    return 0;
}


void Camera::setSaturation(int){
}

/** WhiteBalance methods **/
const char* Camera::getWhitebalMode(){
    return NULL;
}

void Camera::setWhitebalMode(whitebal::WhitebalMode wb){
}

void Camera::setWhitebalAutoMode(whitebal::WhitebalAutoMode wam,int value){
}

const char* Camera::getWhitebalAutoMode(){
    return NULL;
}

int Camera::getWhitebalValueRed(){
    return 0;
}

void Camera::setWhitebalValueRed(int value){
}

int Camera::getWhitebalValueBlue(){
    return 0;
}

void Camera::setWhitebalValueBlue(){
}

/** general methods **/
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

    PvCaptureWaitForFrameDone(this->cam, &frame, PVINFINITE);
    PvCaptureQueueFrame(this->cam, &frame, NULL);

    return PyArray_SimpleNewFromData(CHANNEL,dims,NPY_UINT8,array);
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





