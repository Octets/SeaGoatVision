/* #############################################################################
 * Copyright (C) 2014 Octets - octets.etsmtl.ca
 *
 * This file is part of SeaGoatVision.
 *
 * SeaGoatVision is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 * #############################################################################
 */

#include "opencv2/opencv.hpp"
#include <vector>

#define DOCSTRING "HDR - in C++ using weighted Gaussian distribution"

//const char* CONVERSION = "Convert choice";
//const char* CONV_DESC = "0 = BGR TO YUV\n1 = BGR TO HSV";

const char* EXPOSURE_0 = "Exposure0";
const char* EXPOSURE_0_DESC = "Longest exposure in microseconds";
const char* EXPOSURE_1 = "Exposure1";
const char* EXPOSURE_1_DESC = "2nd exposure length in microseconds";
const char* EXPOSURE_2 = "Exposure2";
const char* EXPOSURE_2_DESC = "3rd exposure length in microseconds ";
const char* EXPOSURE_3 = "Exposure3";
const char* EXPOSURE_3_DESC = "Shorted exposure length in microseconds";

const char* HDR_CONFIDENCE = "Confidence";
const char* HDR_CONFIDENCE_DESC = "Confidence";
const double HDR_CONFIDENCE_DEFAULT = 34.0;

const char* HDR_DARE = "Dare";
const char* HDR_DARE_DESC = "% of maximal luminance for longest exposition";
const double HDR_DARE_DEFAULT = 80.0;

const double MAX_LUMINANCE = 100.0;

//DEBUG PARAMS

const char* SHOW_HDR_LUMINANCE = "Show HDR luminance";

using namespace cv;
using namespace std;

Mat last_rendering;
vector<Mat> images;
vector<Mat> images_buffer;
vector<int> exposures;

// FORWARD DECLARATIONS

cv::Mat weighted(cv::Mat, double, double);
double betha(double, int);

cv::Mat weighted(cv::Mat luminance, double betha, double confidence){
    luminance -= betha;
    cv::pow(luminance, 2, luminance);
    luminance *= -1;
    luminance /= (2.0f * pow(confidence,2));
    cv::exp(luminance, luminance);
    return luminance;
}

//TODO: return k/exposure by finding k thru HDR_DARE
double betha(double dare, int exposure){
    return (dare*255);
}

void init()
{
    param_int(EXPOSURE_0, 3125*4, 0, 30000);
    param_set_desc(EXPOSURE_0, EXPOSURE_0_DESC);
    param_int(EXPOSURE_1, 3125*2, 0, 30000);
    param_set_desc(EXPOSURE_1, EXPOSURE_1_DESC);
    param_int(EXPOSURE_2, 3125, 0, 30000);
    param_set_desc(EXPOSURE_2, EXPOSURE_2_DESC);
    param_int(EXPOSURE_3, 1560, 0, 30000);
    param_set_desc(EXPOSURE_3, EXPOSURE_3_DESC);
    
    param_bool(SHOW_HDR_LUMINANCE, 0);
    
    param_double(HDR_CONFIDENCE, HDR_CONFIDENCE_DEFAULT, 0.0, MAX_LUMINANCE);
    param_set_desc(HDR_CONFIDENCE, HDR_CONFIDENCE_DESC);

    param_double(HDR_DARE, HDR_DARE_DEFAULT, 0.0, 100.0);
    param_set_desc(HDR_DARE, HDR_DARE_DESC);
    
    images.reserve(4);
    images_buffer.reserve(4);
}

cv::Mat execute(cv::Mat image)
{
    exposures.clear();
    exposures.push_back(param_get_int(EXPOSURE_0));
    exposures.push_back(param_get_int(EXPOSURE_1));
    exposures.push_back(param_get_int(EXPOSURE_2));
    exposures.push_back(param_get_int(EXPOSURE_3));

    double dare = param_get_double(HDR_DARE) / 100.0;
    double confidence = param_get_double(HDR_CONFIDENCE) / 100.0;
    
    bool debug_show_hdr_luminance = param_get_bool(SHOW_HDR_LUMINANCE);
    
    if(images_buffer.size() < 4){
        Mat hsv_image;
        cv::cvtColor(image, hsv_image, CV_BGR2HSV);
        images_buffer.push_back(hsv_image);
    }
    if(images_buffer.size() >= 4){
        images.clear();
        images.insert(images.begin(), images_buffer.begin(), images_buffer.end());
        images_buffer.clear();
    }
    if(images.size() >= 4){
        Mat hdr_luminance;
        for(int i=0; i<4; i++){
            double b = betha(dare, exposures[i]);
//            double b = 127.0;
            Mat hsv_channels[3];
            split(images[i], hsv_channels);
            cv::add(hdr_luminance, weighted(hsv_channels[2], b, confidence), hdr_luminance);
        }
        hdr_luminance /= 4;
        
        if(debug_show_hdr_luminance != 0){
            Mat c[3];
            c[0] = hdr_luminance;
            c[1] = hdr_luminance;
            c[2] = hdr_luminance;
            merge(c,3,image);
            return image;
        }
    
        Mat channels[3];
        split(image, channels);
        channels[2] = hdr_luminance;
        merge(channels,3,image);
        cv::cvtColor(image, image, CV_HSV2BGR);
        last_rendering = image;
    }else{
//        image = last_rendering;
    }

    return image;
}