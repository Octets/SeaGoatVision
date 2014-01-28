#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
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

# This file contain configuration about server.py


# from SeaGoatVision.commons import global_env
# if you need to know if you start in local, use next function call
# global_env.get_is_local() return True or False
# Uncomment the other camera module when you need it.
# import datetime
from configurations.template_media.conf_webcam import ConfWebcam
from configurations.template_media.conf_imageGenerator import ConfImageGenerator
# from configurations.template_media.conf_firewire import Conf_firewire
# from configurations.template_media.conf_pygame_cam import Conf_pygame_cam

# keep always true for public configuration
# It's useful if you need to disable private config
active_configuration = True
verbose = False

# Log
# no log When log_path is None else put a string path with file_name
log_path = None
# exemple of log_path
# log_path = "/tmp/log_%s.log" %
# datetime.datetime.now().strftime("%Y-%m-%d_%I:%M:%S")

# Networking
# Server tcp output notification
port_tcp_output = 8090


# Media
path_save_record = ""  # empty string will record on root of seagoat project
lst_media = []

# add camera webcam with default value
cam = ConfWebcam()
# cam.name = "Webcam" # already use the default name
lst_media.append(cam)

# add image generator
cam = ConfImageGenerator()
lst_media.append(cam)

# example of firewire
# cam = Conf_firewire()
# cam.guid = 0x123456789
# cam.name = "Firewire"
# lst_media.append(cam)

# exemple of Pygame_cam, alternative of webcam
# cam = Conf_pygame_cam()
# cam.path = "/dev/video0"
# cam.name = "Webcam"
# lst_media.append(cam)

# Filterchain
show_public_filterchain = True


# Filter
show_public_filter = True

# Other


def cmd_on_start(cmd_handler):
    # you can add command directly with the cmdHandler when the server is ready
    pass
