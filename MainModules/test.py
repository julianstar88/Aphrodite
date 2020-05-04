# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
from PyQt5 import QtWidgets

qapp = QtWidgets.QApplication([])

test = QtWidgets.QPushButton()

print(isinstance(test, QtWidgets.QWidget))

qapp.quit()