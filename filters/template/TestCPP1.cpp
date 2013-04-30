#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

/* Need cv::Mat execute(cv::Mat image) to pass image
 * Returning picture can be different of cv::Mat image or the same variable
 *
 */
#define DOCSTRING "C++ Example Test #1"

cv::Mat execute(cv::Mat image)
{
	notify("patatoum");

    //cv::cvtColor(image, image, CV_BGR2HSV);
    cv::cvtColor(image, image, CV_BGR2YUV);
    //std::cout << image << std::endl;
    return image;
}
