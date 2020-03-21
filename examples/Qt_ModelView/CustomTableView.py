# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""


from PyQt5 import QtWidgets, QtGui, QtCore
from CustomHeaderview import CustomHeader
from HelperModules import createCanvas, createQPixmap
from CustomComponents import CustomLabel

class CustomModelView(QtWidgets.QTableView):

    def __init__(self, model, headerLabels, fontSize = 15, fontWeight = "normal"):
        super().__init__()
        self.setModel(model)
        self.setHorizontalHeader(CustomHeader(self))
        self.verticalHeader().hide()

        self.__setHorizontalHeaderLabels(headerLabels, fontSize, fontWeight)
        self.__renderItemToPixmap()


    def __setHorizontalHeaderLabels(self, headerLabels, fontSize, fontWeight):
        qpixmaps = list()

        for i, label in enumerate(headerLabels):
            canvas = createCanvas(label, fontSize = fontSize, fontWeight = fontWeight)
            pixmap = createQPixmap(canvas)
            qpixmaps.append(pixmap)
            self.setColumnWidth(i, pixmap.size().width())

        self.horizontalHeader().qpixmaps = qpixmaps

    def __renderItemToPixmap(self):
        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = 0)
            index = self.model().indexFromItem(item)
            text = item.displayData

            labels = [item[2] for item in item.trainingAlternatives]
            values = "%s~" * len(labels)
            values = values[:-1]
            values = values % tuple(labels)
            superScripts = "^{%s}" % (values)

            labels = [item[1] for item in item.trainingNotes]
            values = "%s~" * len(labels)
            values = values[:-1]
            values = values % tuple(labels)
            subScripts = "_{%s}" % (values)

            mathText = "{itemText}${superScripts}{subScripts}$".format(
                    itemText = text,
                    superScripts = superScripts,
                    subScripts = subScripts
                )

            canvas = createCanvas(mathText, fontSize = 10)
            qpixmap = createQPixmap(canvas)
            label = CustomLabel(qpixmap)
            label.item = item
            item.setData("", role = QtCore.Qt.DisplayRole)
            self.setIndexWidget(index, label)
        self.resizeColumnsToContents()

    def __resizeTable(self):
        pass
