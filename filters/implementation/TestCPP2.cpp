#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING "C++ Example Test #2"

cv::Mat execute(cv::Mat image, py::object notify)
{
    cv::cvtColor(image, image, CV_BGR2YUV);
    //std::cout << image << std::endl;
    return image;
}
