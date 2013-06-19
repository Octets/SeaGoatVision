#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"
#include <fstream>
#include <stdio.h>

#define DOCSTRING "C++ Warp Perspective"

using namespace cv;

int rotationX_ = -160;
int rotationY_ = 0;
int zoom_ = 100;

void init() {

}

void configure() {
}

cv::Mat execute(cv::Mat image)
{
	//Load parameters from file
	//std::ifstream infile("test.txt");
	//infile >> rotationX_ >> rotationY_ >> zoom_;

	const double w = image.cols;
	const double h = image.rows;

	// Projection 2D -> 3D matrix
	Mat A1 = (Mat_<double>(4,3) <<
		1, 0, -w/2,
		0, 1, -h/2,
		0, 0,    0,
		0, 0,    1);

	// Rotation matrices around the X axis
	const double alpha = rotationX_ / 180. * 3.1416 / w;
	Mat RX = (Mat_<double>(4, 4) <<
		1,          0,           0, 0,
		0, cos(alpha), -sin(alpha), 0,
		0, sin(alpha),  cos(alpha), 0,
		0,          0,           0, 1);

	// Rotation matrices around the X axis

	const double beta = rotationY_ / 180. * 3.1416 / h;
	Mat RY = (Mat_<double>(4, 4) <<
		cos(beta),  0,           sin(beta), 0,
		0,			1,			 0, 0,
		-sin(beta), 0,			 cos(beta), 0,
		0,          0,           0, 1);

	// Translation matrix on the Z axis
	const double dist = zoom_ / 100;
	Mat T = (Mat_<double>(4, 4) <<
		1, 0, 0, 0,
		0, 1, 0, 0,
		0, 0, 1, dist,
		0, 0, 0, 1);

	const double f = 1;
	// Camera Intrisecs matrix 3D -> 2D
	Mat A2 = (Mat_<double>(3,4) <<
		f, 0, w/2, 0,
		0, f, h/2, 0,
		0, 0,   1, 0);

	Mat transfo = A2 * (T * (RX * RY * A1));

	Mat destination;

	warpPerspective(image, destination, transfo, image.size(), INTER_CUBIC | WARP_INVERSE_MAP);

	return destination;
}
