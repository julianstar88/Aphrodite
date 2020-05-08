# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""

import numpy as np

a = [[1,2,3], [4,5,6]]
array = np.array(a)
shape = array.shape

for n in range(shape[0]):
    for m in range(shape[1]):
        print(array[n,m])