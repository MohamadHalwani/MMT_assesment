#!/usr/bin/env python

import numpy as np
import cv2
import sys
import pickle
import os

class CheckerBoardChecker:

    def __init__(self):
        checker_board_image = self.generate_CheckerBoard()
        self.manipulate_CheckerBoard(checker_board_image)

    def generate_CheckerBoard(self):
         
        width = 7
        height = 7
        qipan_cell = 32
        
        width_pix = (width + 1) * qipan_cell  # add extra  qipan_cell  for reserve blank
        height_pix = (height + 1) * qipan_cell
       
        image = np.zeros((256, 256, 3), dtype=np.uint8)
        image.fill(255)
        
        #Create display window
        win_name = "qipan"
        cv2.namedWindow("qipan",cv2.WINDOW_AUTOSIZE)
        cv2.imshow(win_name, image)
        color = (255,255,255)
        
        y0 = 0
        fill_color = 0
        for j in range(0,height + 1):
            y = j * qipan_cell
            for i in range(0,width+1):
                #rint(i)
                x0 = i *qipan_cell
                y0 = y
                rect_start = (x0,y0)
        
                x1 = x0 + qipan_cell
                y1 = y0 + qipan_cell
                rect_end = (x1,y1)
                print(x0,y0,x1,y1, fill_color)
                cv2.rectangle(image, rect_start, rect_end,color, 1, 0)
                #print(fill_color)
                image[y0:y1,x0:x1] = fill_color
                if width % 2: 
                    if i != width:
                        fill_color = (0 if ( fill_color == 255) else 255)
                else:
                    if i != width + 1:
                        fill_color = (0 if ( fill_color == 255) else 255)
   
        cv2.imwrite("qipan_%d_W_%d_H.jpg"%(width, height),image)
        cv2.imshow(win_name, image)
        cv2.waitKey()

        return image

    def manipulate_CheckerBoard(self, checker_board_image):
        for num1 in range(4):
            for num2 in range(4):
                print("num1 is ", num1)
                print("num2 is ", num2)
                print("remainder num1", num1 % 2)
                print("remainder num2", num2 % 2)
                if num1 % 2:
                    if num2 % 2:
                        checker_board_image[0+num1*64:64+num1*64, 0+num2*64:64+num2*64] = (255,255,255)
                    else:
                        checker_board_image[0+num1*64:64+num1*64, 0+num2*64:64+num2*64] = (0,0,0)
                else:
                    if num2 % 2:
                        checker_board_image[0+num1*64:64+num1*64, 0+num2*64:64+num2*64] = (0,0,0)
                    else:
                        checker_board_image[0+num1*64:64+num1*64, 0+num2*64:64+num2*64] = (255,255,255)

        cv2.imshow('Image', checker_board_image)
        cv2.waitKey(0)
                



if __name__ == '__main__':

    CheckerBoardChecker()
    exit()