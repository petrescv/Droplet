# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:04:15 2017

@author: Vlad Petrescu
contact: petrescv@gmail.com
web:     vladpetrescu.wordpress.com
"""

import numpy as np
import matplotlib.pyplot as plt

data_rad = np.load('data_rad.npy')
data_dist = np.load('data_dist.npy')


g = 9.81
rho_l = 998.21
rho_a = 1.225

dia_fit = [   -5.44736556,  1097.99679143]

vel_fit = [   -0.00698848,  4.24670866]

x = np.arange(60,160,1)

d = (dia_fit[0]*x + np.ones(len(x))*dia_fit[1])*1e-6

V = (vel_fit[0]*x + np.ones(len(x))*vel_fit[1])

a = (g*rho_l*np.pi/6.)*d**3 - (rho_a*np.pi*0.075)*d**2*V**2

a_min = min(a)

v = np.sqrt(np.ones(len(x))*V[0]**2 + 2*a_min*(x-np.ones(len(x))*60))


#plt.plot(x,a)
plt.plot(x,v)