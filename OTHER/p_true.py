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



p = [2,4,6,8,10]
h = [60,75,90,100,120,130,150]



def get_p_true():
    
    p_true = []
    for i in range(11):
        p_true.append([])
    for i in range(11):
        for j in range(151):
            p_true[i].append([])
    
    for i in p:
        for j in h:
            if (i==2 and j==60) or (i==4 and j ==60):
                continue
    
            path = '/home/vlad/Desktop/DATA/Labview/Measurements/output_p=' + str(i) + '_h=' + str(j) + '.csv'
            with open(path) as f:
                lines = f.readlines()
            line = [k.strip() for k in lines[0].split(',')]
            p_true[i][j] = float(line[-1])*5.398 - 10.92
        
