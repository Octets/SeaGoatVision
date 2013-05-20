#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
#
#    This file is part of CapraVision.
#    
#    CapraVision is free software: you can redistribute it and/or modify
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

import cv2
import cv2.cv as cv
import numpy as np

class Histogram:
    
    def __init__(self):
        self.debug = False
    
    def execute(self, image):

        hsv = cv2.cvtColor(image,cv2.cv.CV_BGR2HSV)
        b,g,r = cv2.split(image)
        h,s,v = cv2.split(hsv)
        
        ht = self.remove_flood_value(h)
        st = self.remove_flood_value(s)
        vt = self.keep_unique_value(v)
        
        #dilate all channels
        k = 8
        ht = self.dilate(ht, k)
        st = self.dilate(st, k)
        vt = self.dilate(vt, k)
        
        result = ht & st & vt
        
        #blur
        result = cv2.medianBlur(result, 7)
        
        return result
        #cv2.imshow('thresholded',result)
        #cv2.waitKey(0)

    def remove_flood_value(self, channel):
    
        peaks = self.find_peaks(channel, 20)
        #print peaks
        #keep bigger peak only
        maxPeak = peaks[0]
        for peak in peaks:
            if peak[1] - peak[0] > maxPeak[1] - maxPeak[0]:
                maxPeak = peak

        #Thresold with found peak
       #print "Thresholding between " + str(maxPeak)
        channel = cv2.inRange(channel, np.array([maxPeak[0]]), np.array([maxPeak[1]]))

        #invert image
        retval, channel = cv2.threshold(channel, 1, 255, cv2.THRESH_BINARY_INV)
        
        return channel
        
    def keep_unique_value(self, channel):
    
        peaks = self.find_peaks(channel, 35)

        #keep smaller peak only
        minPeak = peaks[0]
        for peak in peaks:
            if peak[1] - peak[0] <= minPeak[1] - minPeak[0]:
                minPeak = peak

        #Thresold with found peak
        #print "Thresholding between " + str(minPeak)
        channel = cv2.inRange(channel, np.array([minPeak[0]]), np.array([minPeak[1]]))

        return channel

    def find_peaks(self, channel, peak_height):
        #generate histogram
        bins = np.arange(256).reshape(256,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
        hist_item = cv2.calcHist([channel],[0],None,[256],[1,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))

        if self.debug:
            #create and show histogram
            output = np.zeros((300,256,3))
            pts = np.column_stack((bins,hist))
            cv2.polylines(output,[pts],False,1)

            output=np.flipud(output)
             
            cv2.imshow('Initial normalized histogram',output)
            cv2.moveWindow('Initial normalized histogram', 1300, 0)

        #truncate histogram with a threshold
        for i in range(0, len(hist)-1):
            if hist[i] <= peak_height:
                hist[i] = 0
            else:
                hist[i] = 255

        if self.debug:
            #create and show histogram
            output = np.zeros((300,256,3))
            pts = np.column_stack((bins,hist))
            cv2.polylines(output,[pts],False,1)

            output=np.flipud(output)
             
            cv2.imshow('Thresholded histogram',output)
            cv2.moveWindow('Thresholded histogram', 1300, 500)

        #detect peaks
        inPeak = False
        peaks = []
        currentPeak = ()
        np.append(hist, 0)
        for i in range(0, len(hist)):
            if hist[i] == 0:
                if inPeak:
                    inPeak = False
                    currentPeak += (i,)
                    peaks.append(currentPeak)
                    currentPeak = ()
            else:
                if not inPeak:
                    inPeak = True
                    currentPeak += (i,)
        
        return peaks
        
        # TODO merge peaks close to each other
        
        #merge close peaks
        #distance_to_merge = 5
        #merged_peaks = []
        #for i in range(0, len(peaks) - 2):
        #    end_of_peak = self.get_end(peaks, 0, distance_to_merge)
        #    merged_peaks.append((peaks[i][0], end_of_peak))
                
        #remove peaks inside each other
        #for peak in peaks:
        #    if peak
        
        #print merged_peaks
        
#        return merged_peaks
        
#    def get_end(self, peaks, start_index, dist):
        #if not (start_index > len(peaks) - 2):
#            if peaks[start_index+1][0] - peaks[start_index][1] <= dist:
#                end = self.get_end(peaks, start_index+1, dist)
#                return end
#                
#        return peaks[start_index][1]

    def dilate(self, img, k):
        kdilate = cv2.getStructuringElement(
                 cv2.MORPH_RECT, 
                 (k,k))
        return cv2.dilate(img, kdilate)
    
