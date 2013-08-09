#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

/* Need cv::Mat execute(cv::Mat image) to pass image
 * Returning picture can be different of cv::Mat image or the same variable
 *
 */
#define DOCSTRING "C++ Example Test #1"

void init() {
	/* Example of parameter */
	param_int("x", 30, 0, 255);
	param_bool("enable", true);
	param_double("ff", 55.5, 0, 60.5);
}

void configure() {
	/* optional function */
	printf("I configure myself.\n");
}

void destroy() {
	/* optional function */
	printf("I destroy myself.\n");
}

cv::Mat execute(cv::Mat image)
{
	/* send a char * */
	notify("patatoum");
	/* or send a string
	notify_str("patatoum2");
	*/

	/* To retrieve original image of the filterchain
	 * cv::Mat image_original = get_image_original();
	 */

    //cv::cvtColor(image, image, CV_BGR2HSV);
    cv::cvtColor(image, image, CV_BGR2YUV);
    //std::cout << image << std::endl;
    return image;
}
