# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:20:29 2020

@author: Julian
"""

l = []

for i in range(6):
    index = i+1
    d = {"id":index, 
         "label":str(index),
         "short": "short %d" % (index),
         "note": "test note %d" % (index)
         }
    l.append(d)

values = list(l[0].values())

    

