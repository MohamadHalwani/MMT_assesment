#!/usr/bin/env python

import numpy as np
import time
import cv2
import sys
import pickle
import os
import math

class DepthEstimator:

    def __init__(self):
        self.focal_length_not_available = True
        self.Focal_length = 0
        video = cv2.VideoCapture(0)

        while True:
            self.read_webcam_feed(video)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        cv2.destroyAllWindows

    def read_webcam_feed(self, video):
        check, frame = video.read()
        #print(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("LIVE WEBCAM FEED", gray)

        # Search for the sticky note
        self.check_for_rectangles(gray, frame)


    def check_for_rectangles(self, gray, rgb):
        gray = cv2.convertScaleAbs(gray)
        edges = cv2.Canny(gray, 10, 250)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        _, contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        IS_FOUND = 0
    
        for cont in contours:
            if cv2.contourArea(cont) > 5000:
                arc_len = cv2.arcLength(cont, True)
                corners = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
                if len(corners) == 4:
                    #input(" Please put the object in 30cm far, then press Enter to Continue")
                    if self.focal_length_not_available:
                        raw_input(" Please put the object in 30cm far, then press Enter to Continue")
                        self.Focal_length = self.find_focal_length(corners)
                        self.focal_length_not_available = False

                    IS_FOUND = 1
                    cv2.drawContours(rgb, [corners], -1, (0, 0, 255), 2)
                    
                    Distance, center_point= self.calculate_Distance(corners)
                    cv2.putText(rgb, "%.2fcm" % Distance,(center_point[0]+10, center_point[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    print(center_point)
                    cv2.circle(rgb, (center_point[0], center_point[1]), 3, (0, 0, 255), -1)
                else:
                    pass

        cv2.namedWindow('edges')
        cv2.imshow('edges', edges)

        cv2.namedWindow('rgb')
        cv2.imshow('rgb', rgb)
        time.sleep(0.1)

    def calculate_pixel_width(self, corners):
        Point1 = [corners[0][0][0], corners[0][0][1]]
        Point2 = [corners[1][0][0], corners[1][0][1]]
        Point3 = [corners[2][0][0], corners[2][0][1]]
        Point4 = [corners[3][0][0], corners[3][0][1]]
        center_point = [(Point1[0]+Point2[0]+Point3[0]+Point4[0])/4, (Point1[1]+Point2[1]+Point3[1]+Point4[1])/4]
        pixel_value = math.sqrt(pow(Point1[0]-Point2[0], 2) + pow(Point1[1]-Point2[1], 2))
        return pixel_value, center_point

    def find_focal_length(self, corners):
        real_distance = 30
        real_width = 6
        pixel_value, _ = self.calculate_pixel_width(corners)
        print("Pixel value is ", pixel_value)
        F = (pixel_value*real_distance)/real_width
        print(" Focal length is", F)
        return F

    def calculate_Distance(self, corners):
        real_width = 6
        pixel_value, center_point = self.calculate_pixel_width(corners)
        D = self.Focal_length*real_width/pixel_value
        print("Distance is ", D)
        return D, center_point





if __name__ == '__main__':

    DepthEstimator()
    exit()