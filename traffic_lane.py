#!/usr/bin/env python
# coding: utf-8

# coding: utf-8


from IPython.display import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt


def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])
def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope = parameters[0]
        intercept = parameters[1]
        #print(image.shape)
      
        if slope <0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
        #print(left_fit)
        #print(right_fit)
        left_fit_average = np.average(left_fit, axis = 0)
        right_fit_average = np.average(right_fit, axis = 0)
        #print(left_fit_average,'leftt')
        #print(right_fit_average,'rightt')
        left_line = make_coordinates(image,left_fit_average)
        right_line = make_coordinates(image,right_fit_average)
        return np.array([left_line,right_line])
        
image = cv2.imread('california-highway.jpeg')
lane_image = np.copy(image)
def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
#cv2.imshow("result",image)
##finding lane ---gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
###finding lane canny---gaussian works internally

    canny = cv2.Canny(blur,50,150)
    return canny
def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1,y1,x2,y2  in lines:
            
            cv2.line(line_image,(x1,y1),(x2,y2),(250,0,0),10)
    return line_image
    
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200,height),(1100,height),(550,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    #6 finding lane line --bitwise
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image


cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _,frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength = 40,maxLineGap = 5)
    averaged_lines = average_slope_intercept(frame,lines)
#lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, 0, minLineLength, 20);
    line_image = display_lines(frame,averaged_lines)
##finding lane line ------region of interest
    combo_image = cv2.addWeighted(frame,0.8,line_image,1,1)
    cv2.imshow('result',combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyallwindows()
print("checking triggerer working or not!)
    
