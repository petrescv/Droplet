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
    
    with open(path_0[:-22] + 'Properties.txt') as f:
        lines = f.readlines()
    
    dt = lines[117][17:47]
    dt = [i.strip() for i in dt.split(',')]
    dt = [float(i) for i in dt][1]
    
    return F0_img, F1_img, path_0[:-22], skip, dt
    
    
def get_distance(pairs,dt):
    
    x_y_0 = np.array(pairs[0])
    x_y_1 = np.array(pairs[1])    
    x_y_squared = (x_y_1 - x_y_0)**2
    
    dist = []
    for i in range(len(x_y_squared)):
        dist.append(np.sqrt(x_y_squared[i][0] + x_y_squared[i][1]))
    
    return np.array(dist)*px_conv/(dt)
    

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




def process(F0_img, F1_img, save_path, n, m, k):

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

            #if rad > rad_lim[n][m][0] and rad < rad_lim[n][m][1]:
            if rad >5 and rad<60:
                centres[j].append((x,y))
                center = (int(x),int(y))
                cv2.circle(new_image_0,center,int(rad),(255,0,0),1)
                centres[j+2].append(rad*2*px_conv)
    
    pairs = find_pairs(centres)
    
    return pairs


    
data_rad = []
for i in range(11):
    data_rad.append([])
for i in range(11):
    for j in range(151):
        data_rad[i].append([])
        
data_count = []
for i in range(11):
    data_count.append([])
for i in range(11):
    for j in range(151):
        data_count[i].append([])

data_dist = []
for i in range(11):
    data_dist.append([])
for i in range(11):
    for j in range(151):
        data_dist[i].append([])


for x in p:
    for y in h:
        
        temp_rad = []
        temp_count = []
        temp_dist = []
        
        if not(x==2 and y==60) and not(x==4 and y ==60):

            for k in range(1,11):
                
                (F0_img, F1_img, save_path, skip, dt) = read(x,y,k)
                
                if not skip:
                    pairs = process(F0_img, F1_img, save_path, x, y, k)
                    
                    radius = np.concatenate((pairs[2],pairs[3]))
                    avg = np.nanmean(radius)
                    radius = radius[radius > avg*0.7]
                    radius = radius[radius < avg*1.3]
                    avg_rad = np.nanmean(radius)                  
                    
                    dist = get_distance(pairs, dt)
                    avg = np.nanmean(dist)
                    dist = dist[dist > avg*0.8]
                    dist = dist[dist < avg*1.2]
                    avg_dist = np.nanmean(dist)
                    
                    temp_count = np.hstack((temp_count, (len(pairs[0]))))
                    temp_rad = np.hstack((temp_rad,avg_rad))#*len(pairs[0])))
                    temp_dist = np.hstack((temp_dist, avg_dist))
                
            radius = temp_rad
            avg = np.nanmean(radius)
            radius = radius[radius > avg*0.8]
            radius = radius[radius < avg*1.2]
            data_rad[x][y] = np.nanmean(radius)
    #        data_rad[x][y] = np.sum(temp_rad)/np.sum(temp_count)
    
            counter = temp_count
            avg = np.nanmean(counter)
            counter = counter[counter > avg*0.9]
            counter = counter[counter < avg*1.1]
            data_count[x][y] = np.nanmean(counter)
            
            dist = temp_dist
    #        print dist
            avg = np.nanmean(dist)
            dist = dist[dist > avg*0.85]       
            dist = dist[dist < avg*1.15]
            data_dist[x][y] = np.nanmean(dist)
    #        data_dist[x][y] = np.nanmean(temp_dist)
            
            print('p=',x,'  h=',y, ' finished')
        







#np.save('data_rad.npy',np.array(data_rad))
#np.save('data_count.npy',np.array(data_count))
#np.save('data_dist.npy',np.array(data_dist))










