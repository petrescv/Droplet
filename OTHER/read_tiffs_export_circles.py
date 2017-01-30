# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:20:11 2017

@author: Vlad Petrescu
contact: petrescv@gmail.com
web:     vladpetrescu.wordpress.com
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import ReadIM
import pylab
import cv2
from scipy import ndimage
import time



p = [6]#,4,6,8,10]
#h = [45,60,75,90,100,120,130,150]
h = [90]  
  
def read(i,j,k):
    
    skip = False
    
    if k == 10:
        k = str(k)
    else:    
        k = '0' + str(k)
        
    path_0 = '/home/vlad/Desktop/DATA/Measurement_p=' + str(i) + '_h=' + str(j) + '/not_filtered_' + k + '_0.tiff'
    path_1 = '/home/vlad/Desktop/DATA/Measurement_p=' + str(i) + '_h=' + str(j) + '/not_filtered_' + k + '_1.tiff'
                
    F0_img = cv2.imread(path_0,0)
    F1_img = cv2.imread(path_1,0)
    
    if F0_img is None:
        skip = True
    
    return F0_img, F1_img, path_0[:-22], skip
    
    
    
    

def find_pairs(centres):
    
    threshold = 8.
    pairs = [[],[],[],[]]
    
    for i in range(len(centres[0])):
        x0 = centres[0][i][0]
        y0 = centres[0][i][1]
        r0 = centres[2][i]
        for j in range(len(centres[1])):
            x1 = centres[1][j][0]
            y1 = centres[1][j][1]
            r1 = centres[3][j]
            
            if abs(x1 - x0) <= threshold and abs(y1 - y0) <= threshold:
                pairs[0].append((x0,y0))
                pairs[1].append((x1,y1))
                pairs[2].append(r0)
                pairs[3].append(r1)
                
    i = 0
    stop = len(pairs[0])
    while (i <= stop-1):
        
        multiple_pairs = [[],[],[],[]]
        multiple_pairs[0].append(pairs[1][i][0])
        multiple_pairs[1].append(pairs[1][i][1])
        multiple_pairs[2].append(pairs[2][i])
        multiple_pairs[3].append(pairs[3][i])
        
        j = i+1
        while (j <= stop-1):
            if pairs[0][i] == pairs[0][j]:
                multiple_pairs[0].append(pairs[1][j][0])
                multiple_pairs[1].append(pairs[1][j][1])
                multiple_pairs[2].append(pairs[2][j])
                multiple_pairs[3].append(pairs[3][j])
                del pairs[0][j]
                del pairs[1][j]
                del pairs[2][j]
                del pairs[3][j]
                stop = stop - 1
                j = j-1
            j = j+1
         
        if len(multiple_pairs[0]) > 1:
            all_x = np.array(multiple_pairs[0]) - pairs[0][i][0]*np.ones(len(multiple_pairs[0]))
            all_y = np.array(multiple_pairs[1]) - pairs[0][i][1]*np.ones(len(multiple_pairs[0]))
            dist = np.sqrt(all_x**2 + all_y**2)
            index_min = np.argmin(dist) 
            pairs[1][i] = (multiple_pairs[0][index_min], multiple_pairs[1][index_min])
            pairs[2][i] = multiple_pairs[2][index_min]
            pairs[3][i] = multiple_pairs[3][index_min]
        i = i + 1
        
        return pairs




def process(F0_img, F1_img, save_path, k):

    new_image_0 = np.ones((1040,1376,3), np.uint8)*255
    
    contours = [[],[]]
    
    blur_0 = cv2.GaussianBlur(F0_img,(5,5),0)
    ret,thresh = cv2.threshold(blur_0,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours[0],hierarchy = cv2.findContours(thresh, 1, 2)
     
    blur_1 = cv2.GaussianBlur(F1_img,(5,5),0)
    ret,thresh = cv2.threshold(blur_1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)  
    contours[1],hierarchy = cv2.findContours(thresh, 1, 2)
    
    
    centres = [[],[],[],[]]
    
    for j in range(len(contours)):
        for i in range(len(contours[j])):
            (x,y),rad = cv2.minEnclosingCircle(contours[j][i])
                
            if rad < 48 and rad > 1.5:
                centres[j].append((x,y))
                center = (int(x),int(y))
                cv2.circle(new_image_0,center,int(rad),(255,0,0),1)
                centres[j+2].append(rad)
    
    pairs = find_pairs(centres)
    
    for i in range(len(pairs[0])):  
        cv2.circle(new_image_0,(int(pairs[0][i][0]), int(pairs[0][i][1])),int(pairs[2][i]),(0,0,255),2)
        cv2.circle(new_image_0,(int(pairs[1][i][0]), int(pairs[1][i][1])),int(pairs[3][i]),(0,0,255),2)
    
    cv2.imwrite(save_path + 'output2_' + str(k) +'.tiff',new_image_0)
    


for x in p:
    for y in h:
        for k in range(1,11):
            
            (F0_img, F1_img, save_path, skip) = read(x,y,k)
            if skip:
                continue                
            process(F0_img, F1_img, save_path, k)
        
        print('p=',x,'  h=',y, ' finished')