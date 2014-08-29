/*
 * Copyright (C) 2014 Octets - octets.etsmtl.ca
 *
 * This file is part of SeaGoatVision.
 *
 * SeaGoatVision is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "opencv2/opencv.hpp"

#define DOCSTRING "C Example Test #1\nConvert BGR color to another color."

const char* CONVERSION = "Convert choice";
const char* CONVERT_DESC = "0 = original\n1 = BGR TO YUV\n2 = BGR TO HSV\n3 = BGR TO RGB\n4 = BGR TO GRAY";

void init()
{
    param_int(CONVERSION, 1, 0, 4);
    param_set_desc(CONVERSION, CONVERT_DESC);
}

cv::Mat execute(cv::Mat image)
{
    int convert_choice = param_get_int(CONVERSION);

    if (convert_choice == 1) {
        cv::cvtColor(image, image, CV_BGR2YUV);
    } else if (convert_choice == 2) {
        cv::cvtColor(image, image, CV_BGR2HSV);
    } else if (convert_choice == 3) {
        cv::cvtColor(image, image, CV_BGR2RGB);
    } else if (convert_choice == 4) {
        // TODO not work because cannot return the new image
        // ticket #111
        cv::cvtColor(image, image, CV_BGR2GRAY);
    }
    return image;
}
