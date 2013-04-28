#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING "C++ Example Test #1"

class TestCPP1 : public Filter {

	int x;

public:

	void init() {
		std::cout << "minit" << std::endl;
		x = ParameterAsInt("x", 0, 255, 30);
	}

	void configure() {
		std::cout << "mconfig" << std::endl;
		x = ParameterAsInt("x", 0, 255, 30);
		std::cout << "config "<< x << std::endl;

	}

	cv::Mat execute(cv::Mat image)
	{

		std::cout << "exec " << x << std::endl;
		cv::cvtColor(image, image, CV_BGR2HSV);
		return image;
	}

};
