/*
 * lib.cpp
 */
#include "lib.h"

void cadabra_filtre(cv::Mat image) {

	cv::cvtColor(image, image, CV_BGR2YUV);
}
