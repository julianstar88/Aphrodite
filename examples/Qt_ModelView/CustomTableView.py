# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""


from PyQt5 import QtWidgets, QtCore
from CustomHeaderview import CustomHeader
from HelperModules import createCanvas, createQPixmap
from CustomComponents import CustomLabel

class CustomModelView(QtWidgets.QTableView):

    ObjectType = "CustomModelView"

    def __init__(self, model, headerLabels, fontSize = 15, fontWeight = "normal", parent = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.setHorizontalHeader(CustomHeader(self))
        self.verticalHeader().hide()

        if parent:
            self.setParent(parent)

        self.__setHorizontalHeaderLabels(headerLabels, fontSize, fontWeight)
        self.__renderItemToPixmap()
        self.__setResizeMode()
        self.__resizeTable()


    def __setHorizontalHeaderLabels(self, headerLabels, fontSize, fontWeight):
        qpixmaps = list()

        for i, label in enumerate(headerLabels):
            canvas = createCanvas(label, fontSize = fontSize, fontWeight = fontWeight)
            pixmap = createQPixmap(canvas)
            qpixmaps.append(pixmap)
            self.setColumnWidth(i, pixmap.size().width())

        self.horizontalHeader().qpixmaps = qpixmaps

    def __setResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Interactive)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def __renderItemToPixmap(self):
        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = 0)
            index = self.model().indexFromItem(item)
            text = item.displayData

            exerciseID = row + 1

            alternatives = [item[2] for item in item.trainingAlternatives if exerciseID == item[1]]
            if alternatives:
                values = "%s~" * len(alternatives)
                values = values[:-1]
                values = values % tuple(alternatives)
                superScripts = "^{%s}" % (values)
            else:
                superScripts = ""

            notes = [item[2] for item in item.trainingNotes if exerciseID == item[1]]
            if notes:
                values = "%s~" * len(notes)
                values = values[:-1]
                values = values % tuple(notes)
                subScripts = "_{%s}" % (values)
            else:
                subScripts = ""

            if alternatives or notes:
                mathText = "{itemText}${superScripts}{subScripts}$".format(
                        itemText = text,
                        superScripts = superScripts,
                        subScripts = subScripts
                    )
            else:
                mathText = "{itemText}".format(
                        itemText = text,
                    )

            canvas = createCanvas(mathText, fontSize = 10)
            qpixmap = createQPixmap(canvas)
            label = CustomLabel(qpixmap)
            label.item = item
            item.setData("", role = QtCore.Qt.DisplayRole)
            self.setIndexWidget(index, label)
        self.resizeColumnToContents(0)

    def __resizeTable(self):
        self.resizeRowsToContents()
        horizontalHeader = self.horizontalHeader()
        verticalHeader = self.verticalHeader()
        headerHeight = horizontalHeader.qpixmaps[0].size().height()

        vsize = []
        for i in range(verticalHeader.count()):
            vsize.append(verticalHeader.sectionSize(i))
        vsize = max(vsize)
        verticalHeader.setMinimumSectionSize(vsize)

        hsize = []
        for i in range(horizontalHeader.count()):
            hsize.append(horizontalHeader.sectionSize(i))
        hsize = max(hsize)
        horizontalHeader.setMinimumSectionSize(hsize)

        tableHeight = verticalHeader.count() * vsize
        tableWidth = horizontalHeader.count() * hsize
        generalHeight = headerHeight + tableHeight

        self.setMaximumHeight(generalHeight)
        self.setMinimumHeight(generalHeight)
        self.setMinimumWidth(tableWidth)

        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().setDisabled(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.parent().setWidget(self)
        self.parent().setMinimumSize(QtCore.QSize(tableWidth, generalHeight))