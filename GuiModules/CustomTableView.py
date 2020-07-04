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
    focusLost = QtCore.pyqtSignal("QWidget", "QFocusEvent")
    keyPressed = QtCore.pyqtSignal("QWidget", "QKeyEvent")
    mousePressed = QtCore.pyqtSignal("QWidget", "QMouseEvent")

    def __init__(self, model, *args,
                 viewParent = None,
                 labelFontSize = 10,
                 labelFontWeight = "normal",
                 labelFontStyle = "normal",
                 labelMargin = 2,
                 headerLabels = None,
                 headerFontSize = 15,
                 headerFontStyle = "normal",
                 headerFontWeight = "normal",
                 exerciseNameColumn = 0,
                 labelMode = "main"):

        super().__init__(*args)
        self._database = None
        self._labelFontSize = None
        self._labelMargin = None
        self._labelFontWeight = None
        self._labelFontStyle = None

        self._headerLabels = None
        self._headerFontSize = None
        self._headerFontWeight = None
        self._headerFontStyle = None

        self._labelMode = None
        self._exerciseNameColumn = None
        self._viewParent = None

        self.setLabelFontSize(labelFontSize)
        self.setLabelMargin(labelMargin)
        self.setLabelFontWeight(labelFontWeight)
        self.setLabelFontStyle(labelFontStyle)

        self.setHeaderLabels(headerLabels)
        self.setHeaderFontSize(headerFontSize)
        self.setHeaderFontWeight(headerFontWeight)
        self.setHeaderFontStyle(headerFontStyle)

        self.setLabelMode(labelMode)
        self.setExerciseNameColumn(exerciseNameColumn)
        self.setViewParent(viewParent)

        # self.setDatabase(database)
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

        # CustomItemDelegate doesn´t work properly yet
        # self.setItemDelegate(CustomDelegate.CustomItemDelegate(self))

        if self.viewParent():
            self.setParent(self.viewParent())

        self.__setHorizontalHeaderLabels()
        self.__setResizeMode()
        self.renderItemToHtml()
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

    def __createLabelText(self, item):
        row = item.row()
        exerciseID = row + 1

        if self.labelMode() == "main":
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

        elif self.labelMode() == "alternative":
            alternative = item.trainingAlternatives[row]
            labelText = "{label}) {itemText}".format(
                    label = alternative[1],
                    itemText = alternative[3],
                )
            return labelText

        else:
            return

    def __createHtmlLabelText(self, item):
        row = item.row()
        exerciseID = row + 1

        if self.labelMode() == "main":
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

        elif self.labelMode() == "alternative":
            alternative = item.trainingAlternatives[row]
            if alternative[0]:
                label = alternative[1] + ")"
            else:
                label = ""
            labelText = "{label} {itemText}".format(
                    label = label,
                    itemText = alternative[3],
                )
            return labelText

        else:
            return

    def __setHorizontalHeaderLabels(self):
        qpixmaps = list()
        labels = self.headerLabels()

        if not labels:
            labels = ["I"] * self.model().columnCount()
            color = "none"
        else:
            color = "black"

        for i, label in enumerate(labels):
            canvas = GraphicUtilityModules.CreateCanvas(
                    label,
                    fontSize = self.headerFontSize(),
                    fontWeight = self.headerFontWeight(),
                    fontColor = color
                )

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

    def exerciseNameColumn(self):
        return self._exerciseNameColumn

    def focusOutEvent(self, event):
        self.focusLost.emit(self, event)
        super().focusOutEvent(event)

    def headerFontSize(self):
        return self._headerFontSize

    def headerFontStyle(self):
        return self._headerFontStyle

    def headerFontWeight(self):
        return self._headerFontWeight

    def headerLabels(self):
        return self._headerLabels

    def keyPressEvent(self, event):
        self.keyPressed.emit(self, event)
        super().keyPressEvent(event)

    def labelFontSize(self):
        return self._labelFontSize

    def labelFontStyle(self):
        return self._labelFontSize

    def labelFontWeight(self):
        return self._labelFontWeight

    def labelMargin(self):
        return self._labelMargin

    def labelMode(self):
        return self._labelMode


    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())

        if event.button() == 1: # left click
            self.__clickModeEvaluation(index)

        elif event.button() == 2: # right click
            self.rightClicked.emit(index)

        super().mouseReleaseEvent(event)

    def mousPressEvent(self, event):
        self.mousePressed.emit(self, event)
        super().mousePressEvent(event)

    def renderItemToHtml(self):
        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = self.exerciseNameColumn)
            index = self.model().indexFromItem(item)

            labelText = self.__createHtmlLabelText(item)

            labelFont = QtGui.QFont()
            labelFont.setPointSize(self.labelFontSize())
            label = QtWidgets.QLabel(labelText)
            label.setTextFormat(QtCore.Qt.RichText)
            label.setFont(labelFont)
            label.setMargin(self.labelMargin())
            item.setData("", role = QtCore.Qt.DisplayRole)

            self.setIndexWidget(index, label)

        self.resizeColumnToContents(0)

    def renderItemToPixmap(self):

        for row in range(self.model().rowCount()):
            item = self.model().item(row, column = self.exerciseNameColumn)
            index = self.model().indexFromItem(item)

            labelText = self.__createLabelText(item)

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

    def setExerciseNameColumn(self, col):
        self._exerciseNameColumn = col

    def setHeaderFontSize(self, fontSize):
        self._headerFontSize = fontSize

    def setHeaderFontStyle(self, fontStyle):
        self._headerFontStyle = fontStyle

    def setHeaderFontWeight(self, fontWeight):
        self._headerFontWeight = fontWeight

    def setHeaderLabels(self, labels):
        self._headerLabels = labels

    def setLabelFontSize(self, size):
        self._labelFontSize = size

    def setLabelFontStyle(self, style):
        self._labelFontStyle = style

    def setLabelFontWeight(self, fontWeight):
        self._labelFontWeight = fontWeight

    def setLabelMargin(self, margin):
        self._labelMargin = margin

    def setLabelMode(self, mode):
        self._labelMode = mode

    def setViewParent(self, parent):
        self._viewParent = parent

    def updateView(self):
        self.setColumnHidden(self.model().columnCount()-1, True)
        self.__setResizeMode()
        self.renderItemToHtml()
        self.resizeTable()

    def viewParent(self):
        return self._viewParent

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