# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:14 2020

@author: Julian
"""
import sqlite3
import pathlib2
from GuiModules.CustomGuiComponents import CustomModelItem
from PyQt5 import QtGui, QtCore

class CustomSqlModel(QtGui.QStandardItemModel):

    ObjectType = "CustomSqlModel"
    itemChanged = QtCore.pyqtSignal(CustomModelItem, bool)
    dataChanged = QtCore.pyqtSignal()

    def __init__(self, database = None, table = "training_routine", parent = None,
                 tableStartIndex = 1, valueStartIndex = 1):

        super().__init__(parent)
        self._database = None
        self._table = None
        self._tableData = None
        self._tableStartIndex = None
        self._valueStartIndex = None

        self.setDatabase(database)
        self.setTable(table)
        self.setTableData([])
        self.setTableStartIndex(tableStartIndex)
        self.setValueStartIndex(valueStartIndex)

        self.itemChanged.connect(self.onItemChanged)

    # def commitTableToDatabase(self):
    #     con = sqlite3.connect(self.database)
    #     with con:
    #         c = con.cursor()

    #         sqlCommand = "DROP FROM {name}".format(
    #                 name = self.table
    #             )
    #         c.execute(sqlCommand)

    #         sqlCommand = "SELECT * FROM {name} WHERE id = 1".format(
    #                 name = self.table
    #             )
    #         c.execute(sqlCommand)
    #         data = c.fetchall()
    #         print(data)

    #     # TODO: insert new <table> into databse

    def data(self, index, role):

        item = self.itemFromIndex(index)
        col = item.column()

        if col >= self.valueStartIndex():
            brush = QtGui.QBrush(QtGui.QColor(160,160,160,120), QtCore.Qt.SolidPattern)
            item.setBackground(brush)

        return super().data(index, role)

    def database(self):
        return self._database

    def onItemChanged(self, item, defaultPurpose):
        if defaultPurpose:
            return
        pass

    def populateModel(self):
        path = pathlib2.Path(self.database())
        if not path.is_file():
            return
        con = sqlite3.connect(path)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM {tableName}".format(tableName = self.table())
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()

        CustomModelItem.fetchAlternativesFromDatabase(self.database())
        CustomModelItem.fetchNotesFromDatabase(self.database())

        for row in data:
            l = [CustomModelItem(item) for item in row[self.tableStartIndex():]]
            self.tableData().append(l)

        for row in self.tableData():
            self.appendRow(row)

    def setDatabase(self, database):
        self._database = database

    def setTable(self, table):
        self._table = table

    def setTableData(self, data):
        self._tableData = data

    def setTableStartIndex(self, index):
        self._tableStartIndex = index

    def setValueStartIndex(self, index):
        self._valueStartIndex = index

    def table(self):
        return self._table

    def tableData(self):
        return self._tableData

    def tableStartIndex(self):
        return self._tableStartIndex

    def updateModel(self):
        CustomModelItem.fetchAlternativesFromDatabase(self.database())
        CustomModelItem.fetchNotesFromDatabase(self.database())

        self.removeRows(0, self.rowCount())
        for row in self.tableData():
            itemList = [CustomModelItem(val.userData()) for val in row]
            self.appendRow(itemList)

    def valueStartIndex(self):
        return self._valueStartIndex

if __name__ == "__main__":
    model = CustomSqlModel()