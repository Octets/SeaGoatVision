#include "opencv2/opencv.hpp"
//#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING "Section filter in C++"

int grass_min = 12;
int grass_max = 80;

int kernel_erode_height = 0;
int kernel_erode_width = 0;
int kernel_dilate_height = 0;
int kernel_dilate_width = 0;
int sections = 0;
int min_area = 0;
cv::Mat kerode;
cv::Mat kdilate;

cv::Scalar color = cv::Scalar(255, 255, 255);

void init() {
	grass_min = ParameterAsInt("Grass Minimum", 1, 255, 12);
	grass_max = ParameterAsInt("Grass Maximum", 1, 255, 80);

	kernel_erode_height = ParameterAsInt("Kernel Erode Height", 1, 255, 3);
	kernel_erode_width = ParameterAsInt("Kernel Erode Width", 1, 255, 3);
	kernel_dilate_height = ParameterAsInt("Kernel Dilate Height", 1, 255, 3);
	kernel_dilate_width = ParameterAsInt("Kernel Dilate Width", 1, 255, 3);
	sections = ParameterAsInt("Sections", 1, 10, 5);
	min_area = ParameterAsInt("Minimum Area", 1, 65535, 100);
	kerode = cv::getStructuringElement(cv::MORPH_CROSS,
	                      cv::Size(kernel_erode_width, kernel_erode_height));
	kdilate = cv::getStructuringElement(cv::MORPH_CROSS,
	                      cv::Size(kernel_dilate_width, kernel_dilate_height));
}

void configure() {
	init();
}

void execute_bgr2hsv(cv::Mat image) {
	cv::cvtColor(image, image, CV_BGR2HSV);
}

cv::Mat execute_remgrass(cv::Mat image) {
	std::vector<cv::Mat> chans(3);
	cv::split(image, chans);
	cv::Mat huemin = chans[0].clone();
	cv::Mat huemax = chans[0].clone();
	cv::threshold(chans[0], huemin, grass_min, 255, cv::THRESH_BINARY_INV);
	cv::threshold(chans[0], huemax, grass_max, 255, cv::THRESH_BINARY);
	cv::Mat hue;
	cv::bitwise_or(huemin, huemax, hue);

	return hue;
}

cv::Mat execute_section(cv::Mat hue) {

	cv::erode(hue, hue, kerode);

	int rows = hue.size().height;
	int section_size = rows / sections;

	for(int i=0;i<sections;i++) {
		int start = section_size * i;
		int end = section_size * (i + 1);
		if(end > rows) {
			end = rows;
		}

		cv::Mat section = hue.rowRange(start, end);

	    std::vector<std::vector<cv::Point> > contours;
		std::vector<cv::Vec4i> hierarchy;
		cv::findContours(section, contours, hierarchy, CV_RETR_LIST, CV_CHAIN_APPROX_NONE );
	    section = cv::Mat::zeros(section.size(), section.type());

		std::vector<std::vector<cv::Point> > hull(contours.size());
		for (size_t i = 0; i < contours.size(); i++) {
			cv::convexHull(cv::Mat(contours[i]), hull[i], false);
		}
		for (size_t i = 0; i < contours.size(); i++) {
			double area = abs(cv::contourArea(contours[i]));
			if(area > min_area) {
				cv::drawContours( section, hull, i, color, -1, 8, std::vector<cv::Vec4i>(), 0, cv::Point() );
	        }
	    }
	}

	cv::dilate(hue, hue, kdilate);
	return hue;
}

cv::Mat execute(cv::Mat image) {
	execute_bgr2hsv(image);
	cv::Mat hue = execute_remgrass(image);
	hue = execute_section(hue);
	cv::Mat chans[] = {hue, hue, hue};
	cv::merge(chans, 3, image);
	return image;
}
