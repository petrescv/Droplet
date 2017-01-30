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



p = [6]
#h = [60,75,90,100,120,130,150]
h = [100]

add = np.ones(1040*1376).reshape(1040,1376)*300


for i in p:
    for j in h:
        for k in range(1,11):
            
            path_bk = '/home/vlad/Desktop/DATA/Measurement_p=' + str(i) + '_h=' + str(j) + '/B00001.im7'
            vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList(path_bk)
            v_background, vbuff = ReadIM.extra.buffer_as_array(vbuff)
            del(vbuff)
    
            if k == 10:
                k = str(k)
            else:    
                k = '0' + str(k)
                
            path = '/home/vlad/Desktop/DATA/Measurement_p=' + str(i) + '_h=' + str(j) + '/B000'+ k + '.im7'
            vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList(path)
            v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
            del(vbuff)
        
            F0_array = v_array[0] + add - v_background[0]
            F1_array = v_array[1] + add - v_background[1]

            plt.imsave(path[:-10] + 'not_filtered_' + k + '_0.tiff', F0_array, cmap=cm.Greys_r)
            plt.imsave(path[:-10] + 'not_filtered_' + k + '_1.tiff', F1_array, cmap=cm.Greys_r)            
        
    print('p=',i,'  h=',j, ' finished')