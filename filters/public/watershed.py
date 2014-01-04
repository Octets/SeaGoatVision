
import cv2
import numpy as np
from scipy.ndimage import label
from SeaGoatVision.server.core.filter import Filter
# http://stackoverflow.com/questions/11294859/how-to-define-the-markers-for-watershed-in-opencv


def segment_on_dt(a, img):
    border = cv2.dilate(img, None, iterations=5)
    border = border - cv2.erode(border, None)

    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)
    lbl, ncc = label(dt)
    lbl = lbl * (255 / ncc)
    # Completing the markers now.
    lbl[border == 255] = 255

    lbl = lbl.astype(np.int32)
    cv2.watershed(a, lbl)

    lbl[lbl == -1] = 0
    lbl = lbl.astype(np.uint8)
    return 255 - lbl


class Watershed(Filter):

    def __init__(self):
        Filter.__init__(self)

    def execute(self, image):
        return self.method1(image)

    def method1(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        bin = cv2.morphologyEx(bin, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int))
        result = segment_on_dt(image, bin)

        result[result != 255] = 0
        image[result == 255] = (0, 0, 255)
        return image

    def method2(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        fg = cv2.erode(thresh, None, iterations=2)
        bgt = cv2.dilate(thresh, None, iterations=3)
        ret, bg = cv2.threshold(bgt, 1, 128, 1)
        marker = cv2.add(fg, bg)
        marker32 = np.int32(marker)
        cv2.watershed(image, marker32)
        m = cv2.convertScaleAbs(marker32)
        ret, thresh = cv2.threshold(
            m, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        res = cv2.bitwise_and(image, image, mask=thresh)
        return res
