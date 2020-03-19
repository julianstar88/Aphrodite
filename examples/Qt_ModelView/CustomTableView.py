# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""


from PyQt5 import QtWidgets

class CustomModelView(QtWidgets.QTableView):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.verticalHeader().hide()
        