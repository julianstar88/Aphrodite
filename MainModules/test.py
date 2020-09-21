# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import re

t = "test +1 test, test+1.1test, test42test, test5.3test"
match = re.findall(r"(\+{0,1}\d+\.{0,1}\d*)", t)

out = list()
for val in match:
    plus = re.search("\+", val)
    if plus:
        out.append("{}".format(val))
    else:
        out.append(float(val))