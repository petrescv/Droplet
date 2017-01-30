# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:17:08 2017

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



data_rad = np.load('data_rad.npy')
data_count = np.load('data_count.npy')
data_dist = np.load('data_dist.npy')
color = ['','y','g','b','r','k']

p = [2,4,6,8,10]
h = [60,75,90,100,120,130,150]
h_true = [56, 72, 86, 100.5, 116, 131.5, 161.5]

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



######### diameter vs height with multiple pressure lines #################
#
#h_rad = [[],[],[],[],[],[]]
#
#
#for i in p:
#    if i == 2 or i == 4:
#        h_rad[i/2] = np.polyfit(h_true[1:],data_rad[i,h][1:],1)
#    else:
#        h_rad[i/2] = np.polyfit(h_true,data_rad[i,h],1)
#
#x = np.arange(56,162,1)
#x2 = np.arange(72,162,1)
#
#y_2 = x2*h_rad[1][0] + h_rad[1][1]*np.ones(len(x2))
#plt.plot(x2, y_2, color = 'b')
#for i in h[1:]:
#    plt.plot(h_true[h.index(i)], data_rad[2,i], marker = 'x', color = 'b')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_rad[2,i], marker = 'x', color = 'b', label = 'p = 1.6 bar')
#
#y_4 = x2*h_rad[2][0] + h_rad[2][1]*np.ones(len(x2))
#plt.plot(x2, y_4, color = 'r')
#for i in h[1:]:
#    plt.plot(h_true[h.index(i)], data_rad[4,i], marker = 'o', color = 'r')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_rad[4,i], marker = 'o', color = 'r', label = 'p = 3.3 bar')
#
#y_6 = x*h_rad[3][0] + h_rad[3][1]*np.ones(len(x))
#plt.plot(x, y_6, color = 'y')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_rad[6,i], marker = '^', color = 'y')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_rad[6,i], marker = '^', color = 'y', label = 'p = 5.1 bar')
#
#y_8 = x*h_rad[4][0] + h_rad[4][1]*np.ones(len(x))
#plt.plot(x, y_8, color = 'g')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_rad[8,i], marker = 's', color = 'g')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_rad[8,i], marker = 's', color = 'g', label = 'p = 6.9 bar')
#
#y_10 = x*h_rad[5][0] + h_rad[5][1]*np.ones(len(x))
#plt.plot(x, y_10, color = 'm')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_rad[10,i], marker = 'D', color = 'm')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_rad[10,i], marker = 'D', color = 'm', label = 'p = 8.9 bar')
#
#plt.xlabel('Distance from the nozzle [mm]')
#plt.ylabel('Droplet mean diameter [$\mu m$]')
#plt.xlim([50,170])
#
#plt.legend(loc= 'best')

########## distance/vel vs height with multiple pressure lines #############

#h_dist = [[],[],[],[],[],[]]
#
#for i in p:
#    if i == 2 or i == 4:
#        h_dist[i/2] = np.polyfit(h_true[1:],data_dist[i,h][1:],1)
#    else:
#        h_dist[i/2] = np.polyfit(h_true,data_dist[i,h],1)
#
#x = np.arange(56,162,1)
#x2 = np.arange(72,162,1)
#
#
#
#y_10 = x*h_dist[5][0] + h_dist[5][1]*np.ones(len(x))
#plt.plot(x, y_10, color = 'm')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_dist[10,i], marker = 'D', color = 'm')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_dist[10,i], marker = 'D', color = 'm', label = 'p = 8.9bar')
#        
#y_8 = x*h_dist[4][0] + h_dist[4][1]*np.ones(len(x))
#plt.plot(x, y_8, color = 'g')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_dist[8,i], marker = 's' , color = 'g')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_dist[8,i], marker = 's' , color = 'g', label = 'p = 6.9bar')
#        
#y_6 = x*h_dist[3][0] + h_dist[3][1]*np.ones(len(x))
#plt.plot(x, y_6, color = 'y')
#for i in h:
#    plt.plot(h_true[h.index(i)], data_dist[6,i], marker = '^', color = 'y')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_dist[6,i], marker = '^', color = 'y', label = 'p = 5.1bar')
#        
#y_4 = x2*h_dist[2][0] + h_dist[2][1]*np.ones(len(x2))
#plt.plot(x2, y_4, color = 'r')
#for i in h[1:]:
#    plt.plot(h_true[h.index(i)], data_dist[4,i], marker = 'o', color = 'r')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_dist[4,i], marker = 'o', color = 'r', label = 'p = 3.3bar')
#
#y_2 = x2*h_dist[1][0] + h_dist[1][1]*np.ones(len(x2))
#plt.plot(x2, y_2, color = 'b')
#for i in h[1:]:
#    plt.plot(h_true[h.index(i)], data_dist[2,i], marker = 'x', color = 'b')
#    if i == 150:
#        plt.plot(h_true[h.index(i)], data_dist[2,i], marker = 'x', color = 'b', label = 'p = 1.6bar')
#
#
#plt.xlabel('Distance from the nozzle [mm]')
#plt.ylabel('Velocity [m/s]')
#plt.ylim([1.5,6])
#plt.xlim([50,170])
#
#plt.legend(loc= 'best')


####################### angles vs pressure ###############################

#p = [1.5148251292, 3.2145871281, 4.943901504, 6.8440256936, 8.8082400372]
#angles = [[],[],[],[],[]]
#angles_avg = []
#
#angles[0] = [62.121, 61.663, 61.852, 62.036, 62.044, 61.444, 62.357]
#angles[1] = [59.362, 60.811, 59.591, 60.615, 60.34, 59.478, 60.738]
#angles[2] = [58.403, 59.839, 58.552, 59.975, 59.984]#, 61.188]
#angles[3] = [59.147, 59.792, 58.633, 58.755, 58.534, 59.341]#, 60.325, 60.738]
#angles[4] = [59.076, 59.615, 59.218, 58.792, 58.124, 58.266]
#
#for i in range(len(p)):
#    for j in range(len(angles[i])):
#        plt.scatter(p[i],angles[i][j]/2.)
#        
#for i in range(5):
#    angles_avg.append(np.average(angles[i]))
#
#x = np.arange(1.5148251292,8.9082400372,0.1)
#y = 30.8620539888*x**(-0.0322188126) + 0.4
#
##plt.scatter(p,angles_avg, color = 'r')
#
#plt.xlabel('Pressure [bar]')
#plt.ylabel('Cone angle [deg]')
#
#plt.plot(x,y)