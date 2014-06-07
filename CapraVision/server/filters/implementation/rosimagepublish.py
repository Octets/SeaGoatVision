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

HAS_ROS = True
try:
    import rospy
except:
    print 'rospy module unavailable!'
    HAS_ROS = False

if HAS_ROS:
    import cv_bridge
    import cv2
    import sensor_msgs.msg

    class RosImagePublisher:
        """Publish the image for ROS"""

        def __init__(self):
            self.publisher = rospy.Publisher('ImageArray', sensor_msgs.msg.Image)
            rospy.init_node('VisionRosClient')
            self.bridge = cv_bridge.CvBridge()
            
        def execute(self, image):
            msg = self.bridge.cv2_to_imgmsg(image)
            msg.header.frame_id = 'seagoat'
            
            try:
                self.publisher.publish(msg)
            except BaseException as e:
                print e.message
            
            return image
            
