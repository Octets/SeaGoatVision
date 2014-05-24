#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Description : Implementation of seagoat ros client
"""


import rospy
import signal
import cv2
import cv
from copy import deepcopy

import sys

from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from SeaGoatVision.client.qt.shared_info import SharedInfo


class RosClient:
    def __init__(self, controller, subscriber,
                 host="localhost", islocal=False):
        self.publisher = rospy.Publisher('ImageArray', Image)

        rospy.init_node('VisionRosClient')
        self.controller = controller
        self.subscriber = subscriber
        self.subscriber.start()

        self.shared_info = SharedInfo()
        self.r = rospy.Rate(10)

        self.execution_name = "ros_client"
        self.media_name = "Webcam"
        self.filterchain = "TestRos"
        file_name = self.shared_info.get(SharedInfo.GLOBAL_PATH_MEDIA)
        is_client_manager = False
        self.controller.get_info_media(self.media_name)
        self.controller.get_execution_info(self.execution_name)
        self.controller.get_filterchain_info(self.filterchain)

        self.status = self.controller.start_filterchain_execution(
            self.execution_name,
            self.media_name,
            self.filterchain,
            file_name,
            is_client_manager
        )

        self.controller.add_image_observer(self.update_image, self.execution_name, "Canny-1")
        self.controller.add_output_observer(self.execution_name)

        self.subscriber.subscribe("media.%s" % self.media_name,
                                  self.update_fps)

        print "Ros Client is started!"
        self.active = True
        signal.signal(signal.SIGINT, self.exit)
        while not rospy.is_shutdown() and self.active:
            self.r.sleep()

        self.controller.stop_filterchain_execution(self.execution_name)
        self.subscriber.stop()
        print "Ros Client is stopped!"

    def update_image(self, image):

        msg = CvBridge().cv2_to_imgmsg(image)
        msg.header.frame_id = "seagoat"
        cv2.imshow("image", image)
        cv2.waitKey(10)

        try:
            self.publisher.publish(msg)
        except BaseException as e:
            print e.message

    def update_fps(self, data):
        if type(data) is not dict:
            return
        fps = data.get("fps")
        print "fps: "+str(fps)

    def exit(self, signal, frame):
        print "Ros client is stopping"
        self.active = False




