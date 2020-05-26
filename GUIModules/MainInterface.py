# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:58:37 2020

@author: Julian
"""

import sys
import MainModules.GraphicalEvaluator as ge
import GuiModules.CustomGuiComponents as cc
import UtilityModules.GraphicUtilityModules as gum
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Aphrodite")
        self.mainWidget = cc.CustomWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        labels = ["Name:", "Start:", "End:", "Trainingmode:"]
        values = ["None", "None", "None", "None"]
        self.panel1 = Panel(labels, values, fontSize = 8, split = [1,5])

        labels = ["None:"]
        values = ["None"]
        self.panel2 = Panel(labels, values, fontSize = 8, split = [1,15])

        self.routineTab = RoutineTab()
        self.evaluatorTab = EvaluatorTab()
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.addTab(self.routineTab, "Trainingroutine")
        self.tabWidget.addTab(self.evaluatorTab, "Evaluation")

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addNoteButton = QtWidgets.QPushButton("+")
        self.deleteNoteButton = QtWidgets.QPushButton("-")
        self.buttonLayout.addWidget(self.addNoteButton)
        self.buttonLayout.addWidget(self.deleteNoteButton)

        self.mainLayout.addWidget(self.panel1, 0, 0)
        self.mainLayout.addLayout(self.buttonLayout, 1, 0)
        self.mainLayout.addWidget(self.panel2, 2, 0)
        self.mainLayout.addWidget(self.tabWidget, 0, 1, 3, 1)
        self.mainLayout.setRowStretch(2, 2)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 2)

        self.__connectButtons()

        self.showMaximized()

    def __connectButtons(self):
        self.addNoteButton.clicked.connect(self.addNote)

    def addNote(self, event):
        labels = self.panel2.labels()
        values = self.panel2.values()
        labels.append("None:")
        values.append("123456789-----"*20)
        self.panel2.setLabels(labels)
        self.panel2.setValues(values)
        self.panel2.updatePanel()

    def deleteNote(self, event):
        labels = self.panel2.labels()
        values = self.panel2.values()
        labels.pop()
        values.pop()
        self.panel2.setLabels(labels)
        self.panel2.setValues(values)
        self.panel2.updatePanel()

class Panel(cc.CustomWidget):

    def __init__(self, labels, values,  *args,
                 fontSize = 8,
                 split = [1, 1]):

        super().__init__(*args)
        self._labels = None
        self._values = None
        self._fontSize = None
        self._widgets = None
        self._split = None

        self.setLabels(labels)
        self.setValues(values)
        self.setFontSize(fontSize)
        self.setSplit(split)

        self.__createPanel()

        self.setStyleSheet(
                """
                Panel {background-color: rgba(255,255,255,100%)}
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

        for i,_ in enumerate(self.labels()):
            label = self.labels()[i]
            value = self.values()[i]

            labelString = label
            labelFont = QtGui.QFont()
            labelFont.setBold(True)
            labelFont.setPointSize(self.fontSize())
            labelWidget = QtWidgets.QLabel(labelString)
            labelWidget.setTextFormat(QtCore.Qt.RichText)
            labelWidget.setFont(labelFont)

            valueString = value
            valueFont = QtGui.QFont()
            valueFont.setPointSize(self.fontSize())
            valueWidget = QtWidgets.QLabel(valueString)
            valueWidget.setTextFormat(QtCore.Qt.RichText)

            layout.addWidget(
                    labelWidget, i, 0, QtCore.Qt.AlignLeft
                )
            layout.addWidget(
                    valueWidget, i, 1, QtCore.Qt.AlignLeft
                )
            layout.setColumnStretch(0, self.split()[0])
            layout.setColumnStretch(1, self.split()[1])
            layout.setRowStretch(len(self.labels()), 2)
            self._widgets[i][0] = labelWidget
            self._widgets[i][1] = valueWidget
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

    def setSplit(self, split):
        if not isinstance(split, list):
            raise TypeError(
                    "input {input_name} does not match {type_name}".format(
                            input_name = str(split),
                            type_name = list
                        )
                )
        if len(split) != 2:
            raise ValueError(
                    "there have to be only two elements in 'split'"
                )
        if not isinstance(split[0], int) or not isinstance(split[1], int):
            raise TypeError(
                    "elements of 'split' does not match {type_name}".format(
                            type_name = int
                        )
                )
        self._split = split

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

    def split(self):
        return self._split

    def updatePanel(self):
        for i, line in enumerate(self._widgets):
            for widget in line:
                self.layout().removeWidget(widget)
                widget.deleteLater()

        self.__initiateWidgets()

        for i,_ in enumerate(self.labels()):
            label = self.labels()[i]
            value = self.values()[i]

            labelString = label
            labelFont = QtGui.QFont()
            labelFont.setBold(True)
            labelFont.setPointSize(self.fontSize())
            labelWidget = QtWidgets.QLabel(labelString)
            labelWidget.setTextFormat(QtCore.Qt.RichText)
            labelWidget.setFont(labelFont)

            valueString = value
            valueFont = QtGui.QFont()
            valueFont.setPointSize(self.fontSize())
            valueWidget = QtWidgets.QLabel(valueString)
            valueWidget.setTextFormat(QtCore.Qt.RichText)

            self.layout().addWidget(
                    labelWidget, i, 0, QtCore.Qt.AlignLeft
                )
            self.layout().addWidget(
                    valueWidget, i, 1, QtCore.Qt.AlignLeft
                )
            self.layout().setColumnStretch(0, self.split()[0])
            self.layout().setColumnStretch(1, self.split()[1])
            self.layout().setRowStretch(self.layout().rowCount(), 2)
            self._widgets[i][0] = labelWidget
            self._widgets[i][1] = valueWidget

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
        self.evaluator = ge.GraphicalEvaluator()

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())