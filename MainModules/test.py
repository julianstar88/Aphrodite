# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import re

value = "15 Whlg. frei"
# value = "1/2/3"
# value = "this is a string without any number in it"


match = re.findall(r"\b\d+\b", value)
out = [float(val) for val in match]
if out:
    print(True)
else:
    print(False)

# for testVal in match:
#     try:
#         float(testVal)
#         print(True)
#     except ValueError:
#         print(False)
