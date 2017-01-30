# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 19:22:56 2017

@author: Vlad Petrescu
contact: petrescv@gmail.com
web:     vladpetrescu.wordpress.com
"""

import numpy as np
import matplotlib.pyplot as plt


cm = plt.cm.get_cmap('RdYlBu')
xy = range(20)
z = xy
sc = plt.scatter(xy, xy, c=z, vmin=45, vmax=150, s=35, cmap=cm)
plt.colorbar(sc)
plt.show()