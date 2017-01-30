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

vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('/home/vlad/Desktop/Measurement_p=10_h=75_Date=160714_Time=122319/B00001.im7')
v_background, vbuff = ReadIM.extra.buffer_as_array(vbuff)
del(vbuff)

vbuff, vatts = ReadIM.extra.get_Buffer_andAttributeList('/home/vlad/Desktop/Measurement_p=10_h=75_Date=160714_Time=122319/B00006.im7')
v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)
del(vbuff)


add = np.ones(1040*1376).reshape(1040,1376)
new_array = v_array[1]+add-v_background[1]


image = cv2.imread('test.png',0)

img = cv2.Canny(image,100,200)

cv2.drawContours(img, contours, -1, (0,255,0), 3)

contours, _ = cv2.findContours(img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)


centres = []
for i in range(len(contours)):
  moments = cv2.moments(contours[i])
  if moments['m00'] != 0:
      centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
      cv2.circle(img, centres[-1], 3, (255, 0, 0), -1)

print centres

cv2.imshow('image', img)
cv2.imwrite('output.png',img)
cv2.waitKey(0)




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