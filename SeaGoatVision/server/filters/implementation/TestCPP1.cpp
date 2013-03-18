#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING "C++ Example Test #1"

cv::Mat execute(cv::Mat image, py::object notify)
{
    py::tuple notify_args(1);
    notify_args[0] = "patatoum";
    notify.call(notify_args);

    cv::cvtColor(image, image, CV_BGR2HSV);
    //cv::cvtColor(image, image, CV_BGR2YUV);
    //std::cout << image << std::endl;
    return image;
}
