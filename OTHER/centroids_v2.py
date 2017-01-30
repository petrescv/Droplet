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

new_image_0 = np.zeros((1040,1376,3), np.uint8)
new_image_1 = np.zeros((1040,1376,3), np.uint16)

F0_img = cv2.imread('test_0.png',0)
F1_img = cv2.imread('filtered_1.tiff',0)

contours = [[],[]]

ret,thresh = cv2.threshold(F0_img,127,255,0)
contours[0],hierarchy = cv2.findContours(thresh, 1, 2)

ret,thresh = cv2.threshold(F1_img,127,255,0)
contours[1],hierarchy = cv2.findContours(thresh, 1, 2)



centres = [[],[]]

for j in range(len(contours)):
    for i in range(len(contours[j])):
        moments = cv2.moments(contours[j][i])
        if moments['m00'] != 0 and len(contours[j][i]) >= 5:
            centres[j].append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
            (x,y),radius = cv2.minEnclosingCircle(contours[j][i])
            center = (int(x),int(y))
            radius = int(radius)
            if radius < 30 and radius > 2.1:
                if j == 0:
                    cv2.circle(new_image_0,center,radius,(255,255,255),2)
                    #cv2.circle(new_image_0, centres[j][-1], 3, (255, 0, 0), -1)
                else:
                    cv2.circle(new_image_0,center,radius,(255,0,0),2)
                    #cv2.circle(new_image_0, centres[j][-1], 3, (255, 0, 0), -1)
                

print centres


plt.imshow(new_image_0, cmap = cm.Greys_r)
#plt.imshow(new_image_1, cmap = cm.Greys_r)


cv2.imwrite('output_0.tiff',new_image_0)
cv2.imwrite('output_1.tiff',new_image_1)






#img = cv2.imread('test.png',0)
#ret,thresh = cv2.threshold(img,127,255,0)
#contours,hierarchy = cv2.findContours(thresh, 1, 2)
#
#cnt = contours[0]
#
#area = cv2.contourArea(cnt)
#
#cv2.drawContours(img, contours, -1, (0,255,0), 3)
#
#plt.imshow(img)


#plt.subplot(121),plt.imshow(new_array,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])




#plt.imshow(v_background[0], cmap = cm.Greys_r)
#plt.imshow(v_array[0], cmap = cm.Greys_r)
#plt.imshow(new_array, cmap = cm.Greys_r)

#plt.imsave('test.2.png', new_array, cmap=cm.Greys_r)

#f, axarr = plt.subplots(3, sharex=True)
#axarr[0].imshow(v_background[0], cmap = cm.Greys_r)
#axarr[1].imshow(v_array[0], cmap = cm.Greys_r)
#axarr[2].imshow(new_array, cmap = cm.Greys_r)



#pylab.savefig('foo.tiff')