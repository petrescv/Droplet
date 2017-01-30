# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:28:28 2017

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


delta_t = 20./1e6  #in seconds



p = [2,4,6,8,10]
h = [60,75,90,100,120,130,150]




rad_lim = []
for i in range(11):
    rad_lim.append([])
for i in range(11):
    for j in range(151):
        rad_lim[i].append([])

with open('/home/vlad/Desktop/DATA/radius_min_max.csv') as f:
    lines = f.readlines()

for j in h:
    a = [i.strip() for i in lines[j].split(',')]
    x = [float(i) for i in a]
    for i in p:
        rad_lim[i][j] = (x[i],x[i+1])
        
        
        
        

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
        
    
def get_distance(pairs):
    
    x_y_0 = np.array(pairs[0])
    x_y_1 = np.array(pairs[1])    
    x_y_squared = (x_y_1 - x_y_0)**2
    
    dist = []
    for i in range(len(x_y_squared)):
        dist.append(np.sqrt(x_y_squared[i][0] + x_y_squared[i][1]))
    
    return np.array(dist)
    
def get_velocity(dist):
    
    return dist/delta_t


vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('/home/vlad/Desktop/Measurement_p=10_h=75_Date=160714_Time=122319/B00001.im7')
v_background, vbuff = ReadIM.extra.buffer_as_array(vbuff)
del(vbuff)

vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('/home/vlad/Desktop/Measurement_p=10_h=75_Date=160714_Time=122319/B00006.im7')
v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
del(vbuff)


add = np.ones(1040*1376).reshape(1040,1376)
F0_array = v_array[0] + add - v_background[0]
F1_array = v_array[1] + add - v_background[1]

#plt.imsave('filtered_0.tiff', F0_array, cmap=cm.Greys_r)
#plt.imsave('filtered_1.tiff', F1_array, cmap=cm.Greys_r)
#time.sleep(3)


F0_img = cv2.imread('filtered_0.tiff',0)
F1_img = cv2.imread('filtered_1.tiff',0)


new_image_0 = np.ones((1040,1376,3), np.uint8)*255
new_image_1 = np.ones((1040,1376,3), np.uint8)*255
   
contours = [[],[]]


blur_0 = cv2.GaussianBlur(F0_img,(5,5),0)
ret,thresh_0 = cv2.threshold(blur_0,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#ret,thresh = cv2.threshold(F0_img,127,255,0)
contours[0],hierarchy = cv2.findContours(thresh_0, 1, 2)
 
blur_1 = cv2.GaussianBlur(F1_img,(5,5),0)
ret,thresh_1 = cv2.threshold(blur_1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)  
##ret,thresh = cv2.threshold(F1_img,127,255,0)
contours[1],hierarchy = cv2.findContours(thresh_1, 1, 2)


centres = [[],[],[],[]]

for j in range(len(contours)):
    for i in range(len(contours[j])):
        (x,y),rad = cv2.minEnclosingCircle(contours[j][i])
            
        if rad > rad_lim[10][150][0] and rad < rad_lim[10][150][1]:
            centres[j].append((x,y))
            center = (int(x),int(y))
            cv2.circle(new_image_0,center,int(rad),(0,0,0),1)
            #cv2.circle(new_image_0, centres[j][-1], 3, (255, 0, 0), -1)
            centres[j+2].append(rad)

pairs = find_pairs(centres)

for i in range(len(pairs[0])):  
    cv2.circle(new_image_0,(int(pairs[0][i][0]), int(pairs[0][i][1])),int(pairs[2][i]),(255,0,0),2)
    cv2.circle(new_image_0,(int(pairs[1][i][0]), int(pairs[1][i][1])),int(pairs[3][i]),(255,0,0),2)

plt.imshow(new_image_0, cmap = cm.Greys_r)
#plt.imshow(new_image_1, cmap = cm.Greys_r)


cv2.imwrite('output_1.tiff',new_image_0)
#cv2.imwrite('output_1.tiff',new_image_1)




