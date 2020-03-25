# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3

from CustomComponents import CustomModelItem

from PyQt5 import QtGui, QtCore

class CustomSqlModel(QtGui.QStandardItemModel):

    ObjectType = "CustomSqlModel"

    def __init__(self, database, table = "training_routine", parent = None,
                 tableStartIndex = 1, valueStartIndex = 1):

        super().__init__(parent=parent)
        self.database = database
        self.table = table
        self.data = list()
        self.tableStartIndex = tableStartIndex
        self.valueStartIndex = valueStartIndex

        self.__populateModel()

    def __populateModel(self):
        con = sqlite3.connect(self.database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM {tableName}".format(tableName = self.table)
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()

        CustomModelItem.fetchAlternativesFromDatabase(self.database)
        CustomModelItem.fetchNotesFromDatabase(self.database)

        for row in data:
            l = [CustomModelItem(item) for item in row[self.tableStartIndex:]]
            self.data.append(l)

        for row in self.data:
            self.appendRow(row)

    def data(self, index, role):

        item = self.itemFromIndex(index)
        col = item.column()

        if col >= self.valueStartIndex:
            brush = QtGui.QBrush(QtGui.QColor(160,160,160,120), QtCore.Qt.SolidPattern)
            item.setBackground(brush)

        return super().data(index, role)

