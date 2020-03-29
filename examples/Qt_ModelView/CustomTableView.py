# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore
from CustomHeaderview import CustomHeader
from HelperModules import createCanvas, createQPixmap
from CustomComponents import CustomLabel
from CustomDelegate import CustomItemDelegate

class CustomModelView(QtWidgets.QTableView):

    ObjectType = "CustomModelView"
    leftDoubleClicked = QtCore.pyqtSignal("QModelIndex")
    leftClicked = QtCore.pyqtSignal("QModelIndex")
    rightClicked = QtCore.pyqtSignal("QModelIndex")

    def __init__(self, model, headerLabels = None, parent = None, fontSize = 15, fontWeight = "normal",
                 fontStyle = "normal", exerciseNameColumn = 0, labelMode = "main", *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.model().setParent(self)
        self.setHorizontalHeader(CustomHeader(self))
        self.verticalHeader().hide()
        self.exerciseNameColumn = exerciseNameColumn

        #click mode evaluation
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.clickMode = str()

        self.setItemDelegate(CustomItemDelegate(self))

        if parent:
            self.setParent(parent)

        self.__setHorizontalHeaderLabels(headerLabels, fontSize, fontWeight, fontStyle)
        self.__setResizeMode()

        self.renderItemToPixmap(labelMode)
        self.resizeTable()

        self.leftClicked.connect(self.onSingleLeftClick)
        self.leftDoubleClicked.connect(self.onDoubleLeftClick)
        self.rightClicked.connect(self.onRightClick)

    def __clickModeEvaluation(self, index):

        def __onTimeOut():

            if self.clickMode == "single":
                self.leftClicked.emit(index)

            elif self.clickMode == "double":
                self.leftDoubleClicked.emit(index)

            else:
                pass

            self.timer.disconnect()

        self.timer.timeout.connect(__onTimeOut)

        if self.timer.isActive():
            self.clickMode = "double"

        else:
            self.timer.start()
            self.clickMode = "single"

    def __createLabelText(self, item, mode):
        row = item.row()
        exerciseID = row + 1

        if mode == "main":
            text = item.displayData
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
                labelText = "{itemText}${superScripts}{subScripts}$".format(
                        itemText = text,
                        superScripts = superScripts,
                        subScripts = subScripts
                    )
                return labelText
            else:
                labelText = "{itemText}".format(
                        itemText = text,
                    )
                return labelText

        elif mode == "alternative":
            for alternative in item.trainingAlternatives:
                if exerciseID == alternative[0]:
                    labelText = "{label}) {itemText}".format(
                            label = alternative[2],
                            itemText = alternative[4],
                        )
                    return labelText
        else:
            return

    def __setHorizontalHeaderLabels(self, headerLabels, fontSize, fontWeight, fontStyle):
        qpixmaps = list()

        if not headerLabels:
            headerLabels = ["I"] * self.model().columnCount()
            color = "none"
        else:
            color = "black"

        for i, label in enumerate(headerLabels):
            canvas = createCanvas(label, fontSize = fontSize, fontWeight = fontWeight,
                                  fontColor = color)

            pixmap = createQPixmap(canvas)
            qpixmaps.append(pixmap)
            self.setColumnWidth(i, pixmap.size().width())

        self.horizontalHeader().qpixmaps = qpixmaps

    def __setResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())

        if event.button() == 1: # left click
            self.__clickModeEvaluation(index)

        elif event.button() == 2: # right click
            self.rightClicked.emit(index)

        else:
            super().mouseReleaseEvent(event)

    def renderItemToPixmap(self, labelMode):

        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = self.exerciseNameColumn)
            index = self.model().indexFromItem(item)

            labelText = self.__createLabelText(item, labelMode)

            canvas = createCanvas(labelText, fontSize = 10)
            qpixmap = createQPixmap(canvas)
            label = CustomLabel(qpixmap)
            label.item = item
            item.setData("", role = QtCore.Qt.DisplayRole)

            self.setIndexWidget(index, label)

        self.resizeColumnToContents(0)

    def resizeTable(self):

        horizontalHeader = self.horizontalHeader()
        verticalHeader = self.verticalHeader()
        headerHeight = horizontalHeader.qpixmaps[0].size().height()

        tableHeight = verticalHeader.length()
        tableWidth = horizontalHeader.length()
        generalHeight = 2*headerHeight + tableHeight

        self.setMaximumHeight(generalHeight)
        self.setMinimumHeight(generalHeight)
        self.setMinimumWidth(tableWidth)

    # Slots
    def onSingleLeftClick(self, index):
        print("single left click")

    def onDoubleLeftClick(self, index):
        print("double left click")

    def onRightClick(self, index):
        print("right click")