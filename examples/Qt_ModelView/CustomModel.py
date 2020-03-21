# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3

from CustomComponents import CustomModelItem

from PyQt5 import QtGui

class CustomSqlModel(QtGui.QStandardItemModel):

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.data = list()

        self.__populateModel()

    def __populateModel(self):
        con = sqlite3.connect(self.database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_routine"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()

        for row in data:
            row = row[1:]
            l = list()
            for i, item in enumerate(row):
                if i == 0:
                    modelItem = CustomModelItem(item)
                    modelItem.fetchAlternativesFromDatabase(self.database)
                    modelItem.fetchNotesFromDatabase(self.database)
                    l.append(modelItem)
                else:
                    modelItem = CustomModelItem(item)
                    l.append(modelItem)
            self.data.append(l)
             # l = [CustomModelItem(item) for item in row[1:]]

        for row in self.data:
            self.appendRow(row)

    def data(self, index, role):
        return super().data(index, role)

