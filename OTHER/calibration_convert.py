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



h = [60,75,90,100,120,130,150]

for i in h:
                
    path = '/home/vlad/Desktop/DATA/Calibrations/Calibration_h=' + str(i) + '/B00001.im7'
    vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList(path)
    v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
    del(vbuff)
    img8 = v_array.astype('uint8')

    plt.imsave(path[:-10] + 'not_filtered.tiff', img8[0], cmap=cm.Greys_r)   