#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING "C++ Example Test #1"

const char* CONVERSION = "Convert choice";
const char* CONV_DESC = "0 = BGR TO YUV\n1 = BGR TO HSV";

void init()
{
    param_int(CONVERSION, 0, 0, 1);
    param_set_desc(CONVERSION, CONV_DESC);
}


cv::Mat execute(cv::Mat image)
{
	notify("patatoum");
    int conv_choice = param_get_int(CONVERSION);

    if (conv_choice == 0){
        cv::cvtColor(image, image, CV_BGR2YUV);
    } else if(conv_choice == 1){
        cv::cvtColor(image, image, CV_BGR2HSV);
    }
    //std::cout << image << std::endl;
    return image;
}
