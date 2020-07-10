# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import win32com.client
import inspect
# from comtypes.client import CreateObject

# app = CreateObject("Excel.Application")
app = win32com.client.dynamic.Dispatch("Excel.Application")
app.Visible = False

wb = app.Workbooks.Add()
ws = wb.Worksheets(1)

cell = ws.Cells(1, 1)
cell.Value = "test"
cell.Characters(2, 1).Font.Superscript = True

# print(cell.Characters())
