#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING = "C++ Example";

cv::Mat execute(cv::Mat image)
{
    cv::cvtColor(image, image, CV_BGR2HSV);
    //std::cout << image << std::endl;
    return image;
}
