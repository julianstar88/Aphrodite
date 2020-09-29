"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
from comtypes.client import CreateObject, GetEvents, ShowEvents
from COMEventHandler import ExcelEventHandler
x = CreateObject("Excel.Application")
connection = GetEvents(x, ExcelEventHandler().WorkbookBeforeClose())
x.Visible = True
x.Quit()


