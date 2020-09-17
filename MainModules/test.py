# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 6, 6)
y = [1, 2, None, None, None, None]
mask = [bool(not val) for val in y]
ym = np.ma.masked_array(y, mask = mask)

plt.plot(x, ym, "-r")
plt.xlim(1, 6)