# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""

import sqlite3
from GuiModules.CustomGuiComponents import CustomModelItem
from PyQt5 import QtGui, QtCore

class CustomSqlModel(QtGui.QStandardItemModel):

    ObjectType = "CustomSqlModel"
    itemChanged = QtCore.pyqtSignal(CustomModelItem, bool)

    def __init__(self, database = None, table = "training_routine", parent = None,
                 tableStartIndex = 1, valueStartIndex = 1):

        super().__init__(parent)
        self.database = database
        self.table = table
        self.tableData = list()
        self.tableStartIndex = tableStartIndex
        self.valueStartIndex = valueStartIndex

        self.itemChanged.connect(self.onItemChanged)

    def commitTableToDatabase(self):
        con = sqlite3.connect(self.database)
        with con:
            c = con.cursor()

            sqlCommand = "DROP FROM {name}".format(
                    name = self.table
                )
            c.execute(sqlCommand)

            sqlCommand = "SELECT * FROM {name} WHERE id = 1".format(
                    name = self.table
                )
            c.execute(sqlCommand)
            data = c.fetchall()
            print(data)

        # TODO: insert new <table> into databse

    def data(self, index, role):

        item = self.itemFromIndex(index)
        col = item.column()

        if col >= self.valueStartIndex:
            brush = QtGui.QBrush(QtGui.QColor(160,160,160,120), QtCore.Qt.SolidPattern)
            item.setBackground(brush)

        return super().data(index, role)

    def onItemChanged(self, item, defaultPurpose):
        if defaultPurpose:
            return
        print(item, defaultPurpose)


    def populateModel(self):
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
            self.tableData.append(l)

        for row in self.tableData:
            self.appendRow(row)

if __name__ == "__main__":
    model = CustomSqlModel()