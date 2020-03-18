# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore, QtGui

class CustomBoxLayout(QtWidgets.QBoxLayout):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.setSizeConstraint(QtWidgets.QBoxLayout.SetMinimumSize)
        
class CustomScrollArea(QtWidgets.QScrollArea):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

class CustomModelItem(QtGui.QStandardItem):
    
    def __init__(self, *args):
        super().__init__(*args)
        
        