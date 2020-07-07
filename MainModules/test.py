# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
from openpyxl import Workbook
from xlrd import open_workbook

wb = Workbook()
ws = wb.active

ws["A1"] = "test"
wb.save("test.xlsx")

xwb = open_workbook("test.xlsx")
xws = xwb.sheet_by_index(0)

print(xws)

# xws.write_rich_text(1, 1, ["test"])

xwb.save("test.xlsx")