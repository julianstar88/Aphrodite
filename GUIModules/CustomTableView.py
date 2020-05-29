# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from UtilityModules import CustomDelegate, GraphicUtilityModules
from GuiModules import CustomHeaderView, CustomGuiComponents

class CustomModelView(QtWidgets.QTableView):

    ObjectType = "CustomModelView"
    leftDoubleClicked = QtCore.pyqtSignal("QModelIndex")
    leftClicked = QtCore.pyqtSignal("QModelIndex")
    rightClicked = QtCore.pyqtSignal("QModelIndex")

    def __init__(self, model, *args, headerLabels = None, parent = None, fontSize = 15, fontWeight = "normal",
                 fontStyle = "normal", exerciseNameColumn = 0, labelMode = "main"):

        super().__init__(*args)
        self._labelFontSize = 10
        self._labelMargin = 2

        self.setModel(model)
        self.model().setParent(self)
        self.setHorizontalHeader(CustomHeaderView.CustomHeader(self))
        self.verticalHeader().hide()
        self.exerciseNameColumn = exerciseNameColumn
        self.setColumnHidden(self.model().columnCount()-1, True)

        #click mode evaluation
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.clickMode = str()

        self.setItemDelegate(CustomDelegate.CustomItemDelegate(self))

        if parent:
            self.setParent(parent)

        self.__setHorizontalHeaderLabels(headerLabels, fontSize, fontWeight, fontStyle)
        self.__setResizeMode()

        # self.renderItemToPixmap(labelMode)
        self.renderItemToHtml(labelMode)
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
            text = item.userData()
            alternatives = [item[1] for item in item.trainingAlternatives if exerciseID == item[0]]
            if alternatives:
                values = "%s~" * len(alternatives)
                values = values[:-1]
                values = values % tuple(alternatives)
                superScripts = "^{%s}" % (values)
            else:
                superScripts = ""

            notes = [item[1] for item in item.trainingNotes if exerciseID == item[0]]
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
            alternative = item.trainingAlternatives[row]
            labelText = "{label}) {itemText}".format(
                    label = alternative[1],
                    itemText = alternative[3],
                )
            return labelText

        else:
            return

    def __createHtmlLabelText(self, item, mode):
        row = item.row()
        exerciseID = row + 1

        if mode == "main":
            text = item.userData()
            alternatives = [item[1] for item in item.trainingAlternatives if exerciseID == item[0]]
            if alternatives:
                values = "%s " * len(alternatives)
                values = values[:-1]
                values = values % tuple(alternatives)
                superScripts = "<sup>%s</sup>" % (values)
            else:
                superScripts = ""

            notes = [item[1] for item in item.trainingNotes if exerciseID == item[0]]
            if notes:
                values = "%s " * len(notes)
                values = values[:-1]
                values = values % tuple(notes)
                subScripts = "<sub>%s</sub>" % (values)
            else:
                subScripts = ""

            if alternatives or notes:
                labelText = "{itemText}{superScripts}{subScripts}".format(
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
            alternative = item.trainingAlternatives[row]
            labelText = "{label}) {itemText}".format(
                    label = alternative[1],
                    itemText = alternative[3],
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
            canvas = GraphicUtilityModules.CreateCanvas(label, fontSize = fontSize, fontWeight = fontWeight,
                                  fontColor = color)

            pixmap = GraphicUtilityModules.CreateQPixmap(canvas)
            qpixmaps.append(pixmap)
            self.setColumnWidth(i, pixmap.size().width())

        self.horizontalHeader().qpixmaps = qpixmaps

    def __setResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def labelFontSize(self):
        return self._labelFontSize

    def labelMargin(self):
        return self._labelMargin

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())

        if event.button() == 1: # left click
            self.__clickModeEvaluation(index)

        elif event.button() == 2: # right click
            self.rightClicked.emit(index)

        super().mouseReleaseEvent(event)

    def renderItemToHtml(self, labelMode):
        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = self.exerciseNameColumn)
            index = self.model().indexFromItem(item)

            labelText = self.__createHtmlLabelText(item, labelMode)

            labelFont = QtGui.QFont()
            labelFont.setPointSize(self.labelFontSize())
            label = QtWidgets.QLabel(labelText)
            label.setTextFormat(QtCore.Qt.RichText)
            label.setFont(labelFont)
            label.setMargin(self.labelMargin())
            item.setData("", role = QtCore.Qt.DisplayRole)

            self.setIndexWidget(index, label)

        self.resizeColumnToContents(0)

    def renderItemToPixmap(self, labelMode):

        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = self.exerciseNameColumn)
            index = self.model().indexFromItem(item)

            labelText = self.__createLabelText(item, labelMode)

            canvas = GraphicUtilityModules.CreateCanvas(labelText, fontSize = self.labelFontSize())
            qpixmap = GraphicUtilityModules.CreateQPixmap(canvas)
            label = CustomGuiComponents.CustomLabel(qpixmap)

            # this line was added to store the original item.text()
            # this is now obsolete, because the original text get saved in the
            # items userData-attribute (via item.setUserData) during creation.
            # to make it short: the line can be deleted in a future version.
            #
            # label.itemText = item.data(role = QtCore.Qt.DisplayRole)

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

    def setLabelFontSize(self, size):
        self._labelFontSize = size

    def setLabelMargin(self, margin):
        self._labelMargin = margin

    # Slots
    def onSingleLeftClick(self, index):
        # print("single left click")
        pass

    def onDoubleLeftClick(self, index):
        # print("double left click")
        pass

    def onRightClick(self, index):
        # print("right click")
        pass