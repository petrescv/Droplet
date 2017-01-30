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
from   scipy import ndimage
import time



for i in range(1,11):
    
    if i == 10:
        a = str(i)
        
    else:    
        a = '0' + str(i)

    vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('/home/vlad/Desktop/Cone_angle/Cone_art_p=10_Date=160714_Time=175213/B000' + a + '.im7')
    v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
    del(vbuff)
    
    
    img8 = v_array[0].astype('uint8')
    
    #plt.imshow(img8, cmap = cm.Greys_r)
    
    plt.imsave('/home/vlad/Desktop/Cone_angle/Cone_art_p=10_Date=160714_Time=175213/p_10_' + a + '.png', img8, cmap=cm.Greys_r)
    
    #time.sleep(2)