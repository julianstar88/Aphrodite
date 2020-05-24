# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:58:37 2020

@author: Julian
"""

import sys
import GuiModules.CustomGuiComponents as cc
import UtilityModules.GraphicUtilityModules as gum
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Aphrodite")
        self.mainWidget = cc.CustomWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        labels = ["test1", "test2", "test3"]
        values = ["testText$^1$", "testText$^2$", "testText$^3$"]
        panel1 = Panel(labels, values, fontSize = 12)

        labels = ["test4", "test5", "test6"]
        values = ["testText$^4$", "testText$^5$", "testText$^6$"]
        panel2 = Panel(labels, values, fontSize = 12)

        self.mainLayout.addWidget(panel1,0,0)
        self.mainLayout.addWidget(panel2,1,0)

        self.show()

class Panel(cc.CustomWidget):

    def __init__(self, labels, values,  *args, fontSize = 12):
        super().__init__(*args)
        self._labels = None
        self._values = None
        self._fontSize = None
        self._widgets = None

        self.setLabels(labels)
        self.setValues(values)
        self.setFontSize(fontSize)

        self.__createPanel()

        self.setStyleSheet(
                """
                CustomWidget {background-color: rgba(255,255,255,100%)}
                """
            )

    def __initiateWidgets(self):
        if len(self.values()) != len(self.labels()):
            raise RuntimeError(
                    "labels have to be the same length as values"
                )

        self._widgets = []
        for i in range(len(self.labels())):
            insert = [None, None]
            self._widgets.insert(i, insert)

    def __createPanel(self):
        if len(self.labels()) != len(self.values()):
            raise RuntimeError(
                    "MainInterface.Panel.createPanel: labels must have the same length as values"
                )
        self.__initiateWidgets()

        layout = QtWidgets.QGridLayout()

        for i, val in enumerate(self.labels()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = self.fontSize()
                )
            pixmap = gum.CreateQPixmap(canvas)
            label = cc.CustomLabel(pixmap)
            layout.addWidget(
                    label, i, 0
                )
            self._widgets[i][0] = label

        for i, val in enumerate(self.values()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = self.fontSize(),
                    horizontalAlignment = "left",
                    dpi = 100
                )
            pixmap = gum.CreateQPixmap(canvas)
            label = cc.CustomLabel(pixmap)
            layout.addWidget(
                    label, i, 1
                )
            self._widgets[i][1] = label

        self.setLayout(layout)
        return self

    def fontSize(self):
        return self._fontSize

    def labels(self):
        return self._labels

    def setFontSize(self, size):
        if not isinstance(size, int):
            raise TypeError(
                    "MainInterface.Panel.setFontSize: input <{input_name}> does not match {type_name}".format(
                            input_name = str(size),
                            type_name = int
                        )
                )
        if size < 0:
            raise ValueError(
                    "MainInterface.Panel.setFontSize: input <{input_name}> has to be greater than zero".format(
                            input_name = str(size)
                        )
                )
        self._fontSize = size

    def setLabels(self, labels):
        if not isinstance(labels, list):
            raise TypeError(
                    "Panel.setLabels: input <{input_name}> does not match {type_name}".format(
                            input_name = str(labels),
                            type_name = list
                        )
                )
        self._labels = labels

    def setValues(self, values):
        if not isinstance(values, list):
            raise TypeError(
                    "Panel.setValues: input <{input_name}> does not match {type_name}".format(
                            input_name = str(values),
                            type_name = list
                        )
                )
        self._values = values

    def setWidgetAtPosition(self, widget, rowIndex, columnIndex):
        if not isinstance(widget, QtWidgets.QWidget):
            raise TypeError(
                    "input <{input_name}> for 'widget' does not match {type_name}".format(
                            input_name = str(widget),
                            type_name = QtWidgets.QWidget
                        )
                )
        if rowIndex > len(self.labels()) or rowIndex < 0:
            raise IndexError(
                    "input <{input_name}> for 'rowIndex' is out of range".format(
                            input_name = str(rowIndex)
                        )
                )
        if columnIndex > 2 or columnIndex < 0:
            raise IndexError(
                    "input <{input_name}> for 'columnIndex' is out of range".format(
                            input_name = str(columnIndex)
                        )
                )
        if len(self.labels()) != len(self.values()):
            raise RuntimeError(
                    "the attribrutes 'labels' and 'values' must have the same length"
                )
        toReplace = self.widgetAtPosition(rowIndex, columnIndex)
        self.layout().replaceWidget(toReplace, widget)

    def updatePanel(self):
        if len(self.labels()) != len(self.values()):
            raise RuntimeError(
                    "the attribrutes 'labels' and 'values' must have the same length"
                )

        for i, val in enumerate(self.labels()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = self.fontSize()
                )
            pixmap = gum.CreateQPixmap(canvas)
            self.widgetAtPosition(i, 0).setPixmap(pixmap)

        for i, val in enumerate(self.values()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = self.fontSize()
                )
            pixmap = gum.CreateQPixmap(canvas)
            self.widgetAtPosition(i, 1).setPixmap(pixmap)

    def values(self):
        return self._values

    def widgetAtPosition(self, rowIndex, columnIndex):
        if rowIndex > len(self.labels()) or rowIndex < 0:
            raise IndexError(
                    "input <{input_name}> for 'rowIndex' is out of range".format(
                            input_name = str(rowIndex)
                        )
                )
        if columnIndex > 2 or columnIndex < 0:
            raise IndexError(
                    "input <{input_name}> for 'columnIndex' is out of range".format(
                            input_name = str(columnIndex)
                        )
                )
        if len(self.labels()) != len(self.values()):
            raise RuntimeError(
                    "the attribrutes 'labels' and 'values' must have the same length"
                )
        return self._widgets[rowIndex][columnIndex]

class RoutineTab(cc.CustomWidget):

    def __init__(self, *args):
        super().__init__(*args)

class EvaluatorTab(cc.CustomWidget):

    def __init__(self, *args):
        super().__init__(*args)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())