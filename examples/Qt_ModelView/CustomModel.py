# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3

from CustomComponents import CustomModelItem

from PyQt5 import QtGui, QtCore

class CustomSqlModel(QtGui.QStandardItemModel):
    
    def __init__(self, database, *args):
        super().__init__(*args)
        self.database = database
        self.data = list()
        
        
    def __populateModel(self):
        con = sqlite3.connect(self.database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_routine"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        
        for row in data:
            l = [CustomModelItem(item) for item in row[1:]]
            self.data.append(l)
            
        self.setRowCount = len(self.data)
        self.setColumnCount = len(self.data[0])
        
    
            