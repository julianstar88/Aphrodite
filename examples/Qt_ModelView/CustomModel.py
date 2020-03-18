# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3

from PyQt5 import QtGui

class CustomSqlModel(QtGui.QStandardItemModel):
    
    def __init__(self, database, *args):
        super().__init__(*args)
        self.database = database
        self.data = None
        
        
    def __populateModel(self):
        pass
    
    def __getData(self, tableName):
        con = sqlite3.connect(self.database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM {name}".format(name = tableName)
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        return data
            