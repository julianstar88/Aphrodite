# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3

from CustomComponents import CustomModelItem

from PyQt5 import QtGui

class CustomSqlModel(QtGui.QStandardItemModel):

    ObjectType = "CustomSqlModel"

    def __init__(self, database, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        CustomModelItem.fetchAlternativesFromDatabase(self.database)
        CustomModelItem.fetchNotesFromDatabase(self.database)

        for row in data:

              l = [CustomModelItem(item) for item in row[1:]]
              self.data.append(l)

        for row in self.data:
            self.appendRow(row)

    def data(self, index, role):

        item = self.itemFromIndex(index)

        return super().data(index, role)

