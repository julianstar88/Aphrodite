# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:58:19 2020

@author: Julian
"""

import openpyxl

wb = openpyxl.Workbook()

if type(wb) == openpyxl.Workbook:
    print(True)
else:
    print(False)