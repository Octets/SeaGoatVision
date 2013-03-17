
from scipy import weave
import cv
import numpy
from SeaGoatVision.server.filters.parameter import Parameter
from SeaGoatVision.server.core.filter import Filter

class ScipyExample(Filter):
    """Example on how to use scipy.weave inside filters.
        The code loop inside the entire image
        and reduce the value of each pixels by half"""

    def __init__(self):
        Filter.__init__(self)
        self.Circley = Parameter("Circley", 0, 200, 0)
        self.Circlex = Parameter("Circlex", 0, 200, 0)
        self.colorr = Parameter("colorr", 0, 255, 0)
        self.colorg = Parameter("colorg", 0, 255, 0)
        self.colorb = Parameter("colorb", 0, 255, 255)
        self.param = {"Circlex" : self.Circlex,
                      "Circley" : self.Circley,
                      "colorr" : self.colorr,
                      "colorg" : self.colorg,
                      "colorb" : self.colorb}

    def execute(self, image):
        #self.notify_output_observers("ScipyTestPy: j=6 \n")
        notify = self.notify_output_observers
        param = {}
        for key, value in self.param.items():
            param[key] = value.get_current_value()
        img1 = cv.fromarray(image)
        weave.inline(
        """
        py::tuple notify_args(1);
        notify_args[0] = "patatoum";
        notify.call(notify_args);
        cv::Mat mat(get_cvmat(img1));
        //printf("addr %d %d\\n",  mat.rows, mat.cols);
        //printf("%d\\n", circlex);

        int circlex = (int)PyInt_AsLong(PyDict_GetItemString(param, "Circlex"));
        int circley = (int)PyInt_AsLong(PyDict_GetItemString(param, "Circley"));
        int colorr = (int)PyInt_AsLong(PyDict_GetItemString(param, "colorr"));
        int colorg = (int)PyInt_AsLong(PyDict_GetItemString(param, "colorg"));
        int colorb = (int)PyInt_AsLong(PyDict_GetItemString(param, "colorb"));

        cv::circle(mat, cv::Point(circlex, circley), mat.cols/4, cv::Scalar(colorr, colorg, colorb), -1);
        """,
        arg_names = ['img1', 'notify', 'param'],
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