/************************************************************************************************
 * camera.cpp
 *
 *  Created on: 2013-02-04
 *  Author: Junior Gregoire
 *  E-mail: junior.gregoire@gmail.com
 *
 *  Class Description:
 *      This class have the responsability to make a abstraction of the library PvApi.h
 *      of Allied Technology. PvApi.h is a library use to communicate to this ethernet camera
 *      Manta g-095c. This class is used to simplify the definition of c++-python interface.
 *************************************************************************************************/

#include "camera.h"
#include <iostream>

Camera::Camera()
{
    //This is necessary to use numpy array
    _import_array();

    cam=NULL;
    frame = tPvFrame();
    array = NULL;
    started = false;
    initialized = false;
    videoStarted = false;
}

Camera::~Camera()
{
    cout << "destructor is called!"<<endl;
    if(array!=NULL){
         this->stop();
    }
    if(cam!=NULL){
       this->uninitialize();
    }

}

/** begin Commands methods **/
void Camera::initialize()
{
    if(this->cam != NULL){
        return;
    }
    if(PvInitialize()==ePvErrSuccess)
    {
        cout<<"Camera module for Manta G-95c version 0.993"<<endl;
    } else {
        throw PvApiNotInitializeException();
    }

    time_t initTimer = time(NULL);
    time_t currentTimer = time(NULL);
    double seconds = 0;


    while(PvCameraCount()==0 && seconds<MAX_TIMEOUT){
        currentTimer = time(NULL);
        seconds = difftime(currentTimer,initTimer);
    }



    if(seconds>=MAX_TIMEOUT){
        PvUnInitialize();
        throw CameraNotInitializeException();
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
    initialized = true;
}

void Camera::uninitialize(){
    if(this->cam == NULL){
        return;
    }
    PvCaptureQueueClear(this->cam);
    PvCameraClose(this->cam);
    PvCaptureEnd(this->cam);
    PvUnInitialize();
    this->cam = NULL;
    initialized = false;
}

PyObject* Camera::getFrame()
{
    checkIfCameraIsInitialized();
    if(array==NULL)
    {
        throw CameraNotStartException();
    }

    PvCaptureWaitForFrameDone(this->cam, &frame, PVINFINITE);
    PvCaptureQueueFrame(this->cam, &frame, NULL);
    return PyArray_SimpleNewFromData(CHANNEL,dims,NPY_UINT8,array);
}

PyObject* Camera::getCam(){
    checkIfCameraIsInitialized();
    return PyArray_SimpleNewFromData(CHANNEL,dims,NPY_UINT8,array);
}

void Camera::startVideo(){
    checkIfCameraIsInitialized();

    if(!started){
        start();
    }
    videoStarted = true;
    while(videoStarted){
        PvCaptureWaitForFrameDone(this->cam, &frame, PVINFINITE);
        PvCaptureQueueFrame(this->cam, &frame, NULL);
    }
}

void Camera::stopVideo(){
    videoStarted = false;
    stop();
}


void Camera::start()
{
    checkIfCameraIsInitialized();

    //start camera receiving frame triggers
    PvCommandRun(this->cam, "AcquisitionStart");


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

    frame.ImageBuffer=array;
    started = true;
}

void Camera::stop(){
    if(array == NULL){
        return;
    }
    checkIfCameraIsInitialized();
    PvCommandRun(this->cam, "AcquisitionStop");
    delete array;
    array = NULL;
    started = false;
}


void Camera::loadConfigFile(){
    checkIfCameraIsInitialized();
    PvCommandRun(this->cam,"ConfigFileLoad");
}

void Camera::saveConfigFile(){
    checkIfCameraIsInitialized();
    PvCommandRun(this->cam,"ConfigFileSave");
}

bool Camera::isInitialized(){
    return initialized;
}

bool Camera::isStarted(){
    return started;
}

/** end Commands methods **/
/** Begin Configurations methods **/
void Camera::setPixelFormat(PixelFormat pf){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,"PixelFormat",pixelFormat[pf]);
    setChannel(pf);
}

PixelFormat Camera::getPixelFormat(){
    checkIfCameraIsInitialized();
    long size = 10;
    char table[size];
    PvAttrEnumGet(this->cam,"PixelFormat",table,size,NULL);
    string pf(table);
    return stringToEnum<PixelFormat>(pf,pixelFormat,PFCount);
}

void Camera::setAcquisitionMode(AcquisitionMode am){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,"AcquisitionMode",acquisitionMode[am]);
}

AcquisitionMode Camera::getAcquisitionMode(){
    checkIfCameraIsInitialized();
    long size = 20;
    char table[size];
    PvAttrEnumGet(this->cam,"AcquisitionMode",table,size,NULL);
    string am(table);
    return stringToEnum<AcquisitionMode>(am,acquisitionMode,AMCount);
}

void Camera::setConfigFileIndex(ConfigFileIndex cfi){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,"ConfigFileIndex",configFileIndex[cfi]);
}

ConfigFileIndex Camera::getConfigFileIndex(){
    checkIfCameraIsInitialized();
    long size = 10;
    char table[size];
    PvAttrEnumGet(this->cam,"ConfigFileIndex",table,size,NULL);
    string cfi(table);
    return stringToEnum<ConfigFileIndex>(cfi,configFileIndex,(int)CFICount);
}

int Camera::getTotalBytesPerFrame(){
    checkIfCameraIsInitialized();
    tPvUint32 frameSize;
    PvAttrUint32Get(this->cam, "TotalBytesPerFrame", &frameSize);
    return frameSize;
}

/** End Configurations Commands **/

/** Begin ROI methods**/

int Camera::getHeight(){
    checkIfCameraIsInitialized();
    tPvUint32 height;
    PvAttrUint32Get(this->cam, "Height", &height);
    return height;
}

void Camera::setHeight(int height){
    checkIfCameraIsInitialized();
    PvAttrUint32Set(this->cam,"Height",height);
}

int Camera::getWidth(){
    checkIfCameraIsInitialized();
    tPvUint32 width;
    PvAttrUint32Get(this->cam,"Width",&width);
    return width;
}

void Camera::setWidth(int width){
    checkIfCameraIsInitialized();
    PvAttrUint32Set(this->cam,"Width",width);
}

int Camera::getRegionX(){
    checkIfCameraIsInitialized();
    tPvUint32 regionX;
    PvAttrUint32Get(this->cam,"RegionX",&regionX);
    return regionX;
}

void Camera::setRegiontX(int regionX){
    checkIfCameraIsInitialized();
    PvAttrUint32Set(this->cam,"RegionX",regionX);
}

int Camera::getRegionY(){
    checkIfCameraIsInitialized();
    tPvUint32 regionY;
    PvAttrUint32Get(this->cam,"RegionY",&regionY);
    return regionY;
}

void Camera::setRegionY(int regionY){
    checkIfCameraIsInitialized();
    PvAttrUint32Set(this->cam,"RegionY",regionY);
}
/** End ROI Methods **/
/** Begin Gamma methods **/
float Camera::getGamma(){
    checkIfCameraIsInitialized();
    tPvFloat32 gamma;
    PvAttrFloat32Get(this->cam,"Gamma",&gamma);
    return gamma;
}

void Camera::setGamma(float gamma){
    checkIfCameraIsInitialized();
    if(!checkFloatValue(gamma,0.45)
       && !checkFloatValue(gamma,0.5)
       && !checkFloatValue(gamma,0.7)
       && !checkFloatValue(gamma,1.0)){
        throw GammaOutOfRangeException();
    }
    PvAttrFloat32Set(this->cam,"Gamma",gamma);
}
/** End Gamma Methods **/
/** Begin Exposure methods **/
exposure::ExposureMode Camera::getExposureMode(){
    checkIfCameraIsInitialized();
    long size = 20;
    char table[size];
    PvAttrEnumGet(this->cam,"ExposureMode",table,size,NULL);
    string em(table);
    return stringToEnum<exposure::ExposureMode>(em,exposureMode,exposure::EMCount);
}

void Camera::setExposureMode(exposure::ExposureMode em){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,"ExposureMode",exposureMode[em]);
}

int Camera::getExposureValue(){
    checkIfCameraIsInitialized();
    tPvUint32 exposureValue;
    PvAttrUint32Get(this->cam,"ExposureValue",&exposureValue);
    return exposureValue;
}

void Camera::setExposureValue(int value){
    checkIfCameraIsInitialized();
    exposure::ExposureMode em = getExposureMode();
    if(em != exposure::Manual){
        throw ExposureValueException();
    }
    if(value < 45){
        throw ExposureMinValueException();
    }
    PvAttrUint32Set(this->cam,"ExposureValue",value);
}

void Camera::setExposureAutoMode(exposure::ExposureAutoMode eam,int value){
    checkIfCameraIsInitialized();

    if(eam == exposure::ExposureAutoAlg){
        throw ExposureAutoAlgException();
    }

    if(eam == exposure::ExposureAutoAdjustTol){
        checkIfValueIsAHalfPercent(value);
    }

    if(eam == exposure::ExposureAutoMax || eam == exposure::ExposureAutoMin){
        if(value < 45){
            throw ExposureMinValueException();
        }
    }

    if(eam == exposure::ExposureAutoOutliers){
        if(value < 0 || value > 10000){
            throw ExposureAutoOutliersException();
        }
    }

    if(eam == exposure::ExposureAutoRate || eam == exposure::ExposureAutoTarget){
        checkIfValueIsAPercent(value);
    }

    PvAttrUint32Set(this->cam,exposureAutoMode[eam],value);
}

int Camera::getExposureAutoMode(exposure::ExposureAutoMode eam){
    checkIfCameraIsInitialized();
    if(eam == exposure::ExposureAutoAlg){
        throw ExposureAutoAlgException();
    }

    tPvUint32 value;
    PvAttrUint32Get(this->cam,exposureAutoMode[eam],&value);
    return value;
}

void Camera::setExposureAutoAlgMode(exposure::ExposureAutoAlgMode eaa){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,exposureAutoMode[exposure::ExposureAutoAlg],exposureAutoAlgMode[eaa]);
}

exposure::ExposureAutoAlgMode Camera::getExposureAutoAlgMode(){
    checkIfCameraIsInitialized();
    long size = 10;
    char table[size];
    PvAttrEnumGet(this->cam,"ExposureAutoAlg",table,size,NULL);
    string eaam(table);
    return stringToEnum<exposure::ExposureAutoAlgMode>(eaam,exposureAutoMode,exposure::EAMCount);
}
/** End Exposure Methods **/
/** Begin Gain methods **/
gain::GainMode Camera::getGainMode(){
    checkIfCameraIsInitialized();
    long size = 10;
    char table[size];
    PvAttrEnumGet(this->cam,"GainMode",table,size,NULL);
    string gm(table);

    return stringToEnum<gain::GainMode>(gm,gainAutoMode,gain::GMCount);
}

void Camera::setGainMode(gain::GainMode gm){
    checkIfCameraIsInitialized();
    PvAttrEnumSet(this->cam,"GainMode",gainMode[gm]);
}

void Camera::setGainAutoMode(gain::GainAutoMode gam ,int value){
    checkIfCameraIsInitialized();
    if(gam == gain::GainAutoAdjustTol){
        checkIfValueIsAHalfPercent(value);
    }

    if(gam == gain::GainAutoOutliers || gam == gain::GainAutoRate || gam == gain::GainAutoTarget){
        checkIfValueIsAPercent(value);
    }

    if(gam == gain::GainAutoMax || gam == gain::GainAutoMin){
        if(value <0 || value > 32){
            throw GainOutOfRangeException();
        }
    }
    PvAttrUint32Set(this->cam,gainAutoMode[gam],value);
}

int Camera::getGainAutoMode(gain::GainAutoMode gam){
    checkIfCameraIsInitialized();
    tPvUint32 value;
    PvAttrUint32Get(this->cam,gainAutoMode[gam],&value);

    return value;
}

void Camera::setGainValue(int value){
    checkIfCameraIsInitialized();

    gain::GainMode gm = getGainMode();
    if(gm == gain::Auto){
        throw GainValueException();
    }

    if(value <0 || value > 32){
        throw GainOutOfRangeException();
    }

    PvAttrUint32Set(this->cam,"GainValue",value);
}

int Camera::getGainValue(){
    checkIfCameraIsInitialized();
    tPvUint32 value;
    PvAttrUint32Get(this->cam,"GainValue",&value);
    return value;
}
/** End Gain Methods **/
/** Hue methods **/
float Camera::getHue(){
    checkIfCameraIsInitialized();

    tPvFloat32 value;
    PvAttrFloat32Get(this->cam,"Hue",&value);
    return value;
}

void Camera::setHue(float hue){
    checkIfCameraIsInitialized();

    if(hue < -40 || hue > 40 ){
        throw HueOutOfRangeException();
    }

    PvAttrFloat32Set(this->cam,"Hue",hue);
}

/** Saturation methods **/
float Camera::getSaturation(){
    checkIfCameraIsInitialized();
    tPvFloat32 value;
    PvAttrFloat32Get(this->cam,"Saturation",&value);
    return value;
}


void Camera::setSaturation(float value){
    checkIfCameraIsInitialized();

    if(value > 2 || value < 0){
        throw SaturationOutOfRangeException();
    }

    PvAttrFloat32Set(this->cam,"Saturation",value);
}

/** WhiteBalance methods **/
whitebal::WhitebalMode Camera::getWhitebalMode(){
    checkIfCameraIsInitialized();
    long size = 10;
    char table[size];
    PvAttrEnumGet(this->cam,"WhitebalMode",table,size,NULL);
    string wbm(table);
    return stringToEnum<whitebal::WhitebalMode>(wbm,whitebalMode,whitebal::WMCount);
}

void Camera::setWhitebalMode(whitebal::WhitebalMode wb){
    checkIfCameraIsInitialized();

    PvAttrEnumSet(this->cam,"WhitebalMode",whitebalMode[wb]);
}

void Camera::setWhitebalAutoMode(whitebal::WhitebalAutoMode wam,int value){
    checkIfCameraIsInitialized();

    if(wam == whitebal::WhitebalAutoAdjustTol){
        checkIfValueIsAHalfPercent(value);
    }

    if(wam == whitebal::WhiteAutoRate){
        checkIfValueIsAPercent(value);
    }

    PvAttrUint32Set(this->cam,whiteAutoMode[wam],value);
}


int Camera::getWhitebalAutoMode(whitebal::WhitebalAutoMode wam){
    checkIfCameraIsInitialized();

    tPvUint32 value;
    PvAttrUint32Get(this->cam,whiteAutoMode[wam],&value);

    return value;
}

int Camera::getWhitebalValueRed(){
    checkIfCameraIsInitialized();
    tPvUint32 value;;
    PvAttrUint32Get(this->cam,"WhitebalValueRed",&value);
    return value;
}

void Camera::setWhitebalValueRed(int value){
    checkIfCameraIsInitialized();
    checkWhitebalValue(value);
    PvAttrUint32Set(this->cam,"WhitebalValueRed",value);
}

int Camera::getWhitebalValueBlue(){
    checkIfCameraIsInitialized();
    tPvUint32 value;
    PvAttrUint32Get(this->cam,"WhitebalValueBlue",&value);
    return value;
}

void Camera::setWhitebalValueBlue(int value){
    checkIfCameraIsInitialized();
    checkWhitebalValue(value);
    checkIfValueIsAPercent(value);
    PvAttrUint32Set(this->cam,"WhitebalValueBlue",value);
}



/** private methods **/
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

void Camera::checkIfValueIsAPercent(int value){
    if(value < 0 || value > 100){
        throw FullPercentValueException();
    }
}

void Camera::checkIfValueIsAHalfPercent(int value){
     if(value < 0 || value > 50){
        throw HalfPercentValueException();
    }
}

bool Camera::checkFloatValue(float value, float ref){
    float sigma = 0.01;
    if(value < ref - sigma){
        return false;
    }

    else if (value > ref+sigma){
        return false;
    }

    else {
        return true;
    }
}

void Camera::checkWhitebalValue(int value){
    whitebal::WhitebalMode wbm = getWhitebalMode();
    if(wbm == whitebal::Auto){
        throw WhitebalModeException();
    }
    if(value <80 || value > 300){
        throw WhitebalValueException();
    }
}

void Camera::checkIfCameraIsInitialized(){
    if(this->cam == NULL)
    {
        throw CameraNotInitializeException();
    }
}






