# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import inspect
from comtypes.client import CreateObject

app = CreateObject("Excel.Application")
app.Visible = True

wb = app.Workbooks.Add()
ws = wb.Worksheets[1]

cell = ws.Cells[1 ,1]
cell.Value[:] = "test"
cell.Characters[2, 1].Font.Superscript = True

