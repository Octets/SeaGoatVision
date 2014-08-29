from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter
from PIL import Image
from copy import copy
import numpy as np


class HDR(Filter):

    """High-dynamic-range_imaging with python PIL - works with files"""

    def __init__(self):
        Filter.__init__(self)
        self.case = 'test'
        self.resize = False

        self.strength = Param("strength", 0.0, min_v=0.0, max_v=3.0)
        self.naturalness = Param("naturalness", 10, min_v=0, max_v=10)
        # self.sub_lum = Param("sub_lum", 100, min_v=0, max_v=255)
        # self.shift_x = Param("shift_x", 0, min_v=-800, max_v=800)
        # self.shift_y = Param("shift_y", 0, min_v=-600, max_v=600)

        self.show_image = Param("show_images", 1, min_v=1, max_v=10)
        self.limit_image = Param("limit_image", 4, min_v=1, max_v=10)
        self.debug_show = Param(
            "show_debug",
            "show_normal",
            lst_value=[
                "show_normal",
                "show_sat",
                "show_con"])
        self.show_hdr = Param("show_hdr", False)
        self.index = 0
        self.images = []
        self.imgs = []
        self.first_time = True

    def execute(self, image):
        show_hdr = self.show_hdr.get()
        limit_image = self.limit_image.get()
        len_image = len(self.images)
        if len_image == limit_image:
            self.images[self.index - 1] = image
            self.index += 1
            if self.index > limit_image:
                self.index = 1
        elif len_image < limit_image:
            self.images.append(image)
            self.index += 1
        else:
            self.images.pop()
            if self.index > limit_image:
                self.index = limit_image

        len_image = len(self.images)

        show_no = self.show_image.get()
        show_no = len_image if show_no > len_image else show_no

        if not show_hdr:
            return self.images[show_no - 1]
        nature = self.naturalness.get()
        if nature:
            nature /= 10.0
        return self.get_hdr(self.images, strength=self.strength.get(),
                            naturalness=nature)

    """
    SOURCE: https://sites.google.com/site/bpowah/hdrandpythonpil
    a collection of images to merge into HDR

    blend an arbitrary number of photos into a single HDR image
    or several images with various combinations of HDR parameters

    it is assumed that project folders contain all the images you want to merge
    case = folder name
    cur_dir = folder where the project folders are located
    images are auto-sorted by degree of exposure (image brightness)
    """

    def get_masks(self, imgs, cur_str):
        """
        create a set of masks from a list of images
        (one mask for every adjacent pair of images
        """
        masks = []
        mask_ct = len(imgs) - 1
        imgs = [self.bal(img.convert(mode='L'), cur_str) for img in imgs]
        for i in range(mask_ct):
            blend_fraction = .5  # 1. - (float(i)+.5)/float(mask_ct)
            m = Image.blend(imgs[i], imgs[i + 1], blend_fraction)
            masks.append(m)
        return masks

    def bal(self, im, cur_str):
        """
        adjust the balance of the mask
        (re-distribute the histogram so that there are more
        extreme blacks and whites)
        like increasing the contrast, but without clipping
        and maintains overall average image brightness
        """
        h = im.histogram()
        ln = range(len(h))
        up = [sum(h[0: i]) for i in ln]
        lo = [sum(h[i:-1]) for i in ln]
        ct = sum(h)
        st = int(cur_str * 255.)

        lut = [i + st * up[i] * lo[i] * (up[i] - lo[i]) / ct ** 3 for i in ln]
        for i in ln:
            if lut[i] < 1:
                lut[i] = 1
            if lut[i] > 255:
                lut[i] = 255
        return im.point(lut)

    def merge(self, imgs, cur_str):
        """
        combine a set images into a smaller set by combinding all
        adjacent images
        """
        masks = self.get_masks(imgs, cur_str)
        imx = lambda i: Image.composite(imgs[i], imgs[i + 1], masks[i])
        return [imx(i) for i in range(len(masks))]

    def merge_all(self, imgs, cur_str):
        """
        iteratively merge a set of images until only one remains
        """
        while len(imgs) > 1:
            imgs = self.merge(imgs, cur_str)
        return imgs[0]

    def get_hdr(self, images, strength=0.0, naturalness=1.0):
        """
        process the hdr image(s)
        strength - a float that defines how strong the hdr
                   effect should be
                 - a value of zero will combine images by using a
                   greyscale image average
                 - a value greater than zero will use higher contrast
                   versions of those greyscale images
                 - suggest you a value between 0.0 and 2.0
        naturalness - values between zero and one
                 - zero will be a very high-contrast image
                 - 1.0 will be a very flat image
                 - 0.7 to 0.9 tend to give the best results
        """
        imgs = copy([Image.fromarray(img) for img in images])

        sat_img = self.merge_all(imgs, strength)
        if self.debug_show.get_pos_list() == 1:
            return np.array(sat_img)
        imgs.reverse()

        con_img = self.merge_all(imgs, strength)
        if self.debug_show.get_pos_list() == 2:
            return np.array(con_img)

        """
        combines a saturated image with a contrast image
        and puts them in a dictionary of completed images
        """
        images = Image.blend(con_img, sat_img, naturalness)
        images = np.array(images)
        return images
