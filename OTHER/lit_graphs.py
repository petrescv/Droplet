# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:25:53 2017

@author: Vlad Petrescu
contact: petrescv@gmail.com
web:     vladpetrescu.wordpress.com
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi,sqrt


##################### DEFINING CONSTANTS AT 20 DEG C #####################


E       = 2.1500E9       # Pa       -  Liquid bulk elasticity modulus
nu_L    = 1.0034E-6      # m^2/s    -  Liquid kinematic viscosity
mu_L    = 1.0020E-3      # kg/(ms)  -  Liquid absolute (dynamic) viscosity
rho_L_0 = 9.9821E2       # kg/m^3   -  Liquid density
sigma   = 7.2800E-2      # kg/s^2   -  Liquid surface tension
p_V     = 2.3388E3       # Pa       -  Liquid vapor pressure
mu_A    = 1.8460E-5      # kg(ms)   -  Air absolute (dynamic) viscosity
rho_A   = 1.2041         # kg/m^3   -  Air density


############################ NOZZLE GEOMETRY #############################


d_0     = 11E-3         # m        -  Orifice diameter
l_0     = 10E-3           # m        -  Length of the orifice
A       = 3+0.28*l_0/d_0 # -        -  Geometry constant
Cd      = 0.15           # -        -  Discharge coefficient


######################### PARAMETER DEFINITIONS ##########################


# Define the pressure vessel range from 0 to 100 bar
P_vessel_bar = np.arange(1,11,1)
P_vessel = P_vessel_bar*1e5

# Define pressure drop as the difference between the P_vessel and p_V
delta_P = P_vessel - p_V*np.ones(10)

# Redifine liquid density as a function of pressure
rho_L = rho_L_0/(1-delta_P/E)

# Calculate the exit velocity of the jet
V_e = Cd*np.sqrt(2*delta_P/rho_L)

#Caluclate the volumetric flow rate
Q = V_e*np.pi*(d_0/2)**2

# Defining the Reynolds number
Re = rho_L*V_e*d_0/mu_L

# Defining the Weber number
We = rho_L*V_e**2*d_0/sigma


############################## ANGLE MODELS ##############################


theta_abramovich = 180/pi*np.arctan(0.13*(1+rho_A/rho_L))

theta_reitz = 180/pi*np.arctan(2*pi/sqrt(3*A)*(rho_A/rho_L)**0.5)

theta_ruiz = 180/pi*np.arctan(2*pi/sqrt(3*A)*(rho_A/rho_L)**0.5* \
             (Re/We)**(-0.25))


################################# PLOTS ##################################


plt.plot(P_vessel_bar, theta_abramovich, marker = 'o', 
         markersize=8, markevery=5, markerfacecolor="None", color = 'k', 
         label = 'Abramovich')
plt.plot(P_vessel_bar, theta_reitz,  color = 'k', 
         label = 'Reitz and Bracco')
plt.plot(P_vessel_bar, theta_ruiz, 'k--', label = 'Ruiz and Chigier')
plt.xlabel("Reservoir pressure [bar]",fontsize = 25)
plt.ylabel("$\\theta$ [deg]",fontsize = 25)
axes = plt.gca()
axes.set_ylim([0,30])
plt.legend(loc=2, fontsize = 25)
plt.tick_params(labelsize=25)
plt.grid(True)