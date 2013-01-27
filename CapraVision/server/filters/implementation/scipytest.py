
from scipy import weave
import cv
import numpy

class ScipyExample:
    """Example on how to use scipy.weave inside filters.
        The code loop inside the entire image 
        and reduce the value of each pixels by half"""
    
    def __init__(self):
        pass

    def execute(self, image):
        img1 = cv.fromarray(image)
        weave.inline(
        """
        cv::Mat mat(get_cvmat(img1));
        //printf("addr %d %d\\n",  mat.rows, mat.cols);
        cv::circle(mat, cv::Point(mat.rows/2, mat.cols/2), mat.cols/4, cv::Scalar(255, 0, 0), -1);
        """,
        arg_names = ['img1'],
        include_dirs = ['/usr/local/include/opencv/'],
        headers = ['<cv.h>', '<cxcore.h>'],
        #libraries = ['ml', 'cvaux', 'highgui', 'cv', 'cxcore'],
        extra_objects = ["`pkg-config --cflags --libs opencv`"],
        support_code = """
        struct cvmat_t {
                PyObject_HEAD
                CvMat *a;
                PyObject *data;
                size_t offset;
        };
        CvMat *get_cvmat(PyObject *o) { return ((cvmat_t*)o)->a; }
        """
        )
        img1 = numpy.asarray(img1)
        return img1

