# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import re
import ast

testValues = ["5", "5/5/5", "sdfs", "sfdsdf/sdf/xdf", ""]

match = []
for val in testValues:
    testVal = re.split("/", val)
    for num in testVal:
        try:
            valid = ast.literal_eval(num)
            match.append(valid)
        except (ValueError, SyntaxError):
            match.append(0)

