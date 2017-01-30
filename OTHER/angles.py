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

px_conv = 21./1377.*1000 #in micro meters

p = [2,4,6,8,10]
h = [10]

add = np.zeros(1376*600)
add = add.reshape(600,1376)
add[:,1376/2] = 255
  
def read(i,j,k):
    
    skip = False
    
    if k == 10:
        k = str(k)
    else:    
        k = '0' + str(k)
        
    path_0 = '/home/vlad/Desktop/DATA/Angles/Measurement_p=' + str(i) + '_h=' + str(j) + '/filtered_' + k + '_0.tiff'
    path_1 = '/home/vlad/Desktop/DATA/Angles/Measurement_p=' + str(i) + '_h=' + str(j) + '/filtered_' + k + '_1.tiff'
                
    F0_img = cv2.imread(path_0,0)
    F1_img = cv2.imread(path_1,0)
    
    save_path = path_0[:-18]
    
    return F0_img, F1_img, save_path



def process(F0_img, F1_img, save_path, k):

    blur_0 = cv2.GaussianBlur(F0_img,(5,5),0)
    ret,thresh_0 = cv2.threshold(blur_0,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     
    blur_1 = cv2.GaussianBlur(F1_img,(5,5),0)
    ret,thresh_1 = cv2.threshold(blur_1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)  
    
    if len(thresh_0[0]) == 1376:
        
        thresh_2 = np.vstack((add,thresh_0))
        thresh_3 = np.vstack((add,thresh_1))
        
    if k == 10:
        k = str(k)
    else:    
        k = '0' + str(k)
    
    plt.imsave(save_path + 'angle_' + k + '_0.tiff', thresh_2, cmap=cm.Greys_r)
    plt.imsave(save_path + 'angle_' + k + '_1.tiff', thresh_3, cmap=cm.Greys_r)      

for i in p:
    for j in h:
        for k in range(2,11):
            
            (F0_img, F1_img, save_path) = read(i,j,k)
            process(F0_img, F1_img, save_path, k)
