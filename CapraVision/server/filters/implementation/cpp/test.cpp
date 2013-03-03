#include "opencv2/opencv.hpp"
#include "opencv2/gpu/gpu.hpp"

#define DOCSTRING = "C++ Example";

cv::Mat execute(cv::Mat image)
{
    // The matrix must be uploaded to the gpu before processing
    // This is essential to avoid too much data transfer between cpu and gpu
    cv::gpu::GpuMat gpuimg;
    gpuimg.upload(image);

    // Process image here
    cv::gpu::cvtColor(gpuimg, gpuimg, CV_BGR2HSV);

    // Download result in original matrix
    // The numpy image is modified here.  No further steps are required
    gpuimg.download(image);

    return image;
}
