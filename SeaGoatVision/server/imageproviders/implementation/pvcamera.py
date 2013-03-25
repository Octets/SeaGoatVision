#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This filename is part of SeaGoatVision.
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

USE_PV_CAM = True

try:
    import camera
except:
    print "Cannot open PvCamera.  Missing camera library."
    USE_PV_CAM = False

if USE_PV_CAM:
    class PvNetworkCamera:
        
        def __init__(self):
            self.cam = camera.Camera()
            try:
                self.cam.initialize()
            except:
                pass
            try:
                self.cam.startCamera()
            except:
                pass
            
        def __iter__(self):
            return self
        
        def next(self):
            image = self.cam.getFrame()
            print image
            return image
        
        def close(self):
            pass
    
