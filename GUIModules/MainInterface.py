# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:58:37 2020

@author: Julian
"""

import sys
import re
import pathlib2
import datetime
from MainModules import ConfigInterface, Database, Exporter, GraphicalEvaluator
from UtilityModules import CustomModel
from GuiModules import CustomTableView
import GuiModules.CustomGuiComponents as cc
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args,
                 configParser = None,
                 database = None,
                 evaluator = None,
                 exporter = None,
                 alternativeModel = None,
                 routineModel = None):

        super().__init__(*args)
        self._configParser = None
        self._database = None
        self._evaluator = None
        self._exporter = None
        self._alternativeModel = None
        self._routineModel = None

        self.setConfigParser(configParser)
        self.setDatabase(database)
        self.setEvaluator(evaluator)
        self.setExporter(exporter)
        self.setAlternativeModel(alternativeModel)
        self.setRoutineModel(routineModel)

        self.setWindowTitle("Aphrodite")
        self.mainWidget = cc.CustomWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        generalLabels = ["Name:", "Start:", "End:", "Trainingmode:"]
        generalValues = ["None", "None", "None", "None"]
        noteLabels = ["None:", "None:"]
        noteValues = ["None", "None"]

        if self.database():
            database = Database.database(self.database())

            data = database.data("general_information")[0]
            generalValues = [data[0], data[1], self.__calculateEndData(data[1]), data[2]]

            data = database.data("training_notes")
            noteLabels = list()
            noteValues = list()
            for note in data:
                noteLabels.append(note[1] + ")")
                noteValues.append(note[3])

        self.panel1 = GridPanel(generalLabels, generalValues, fontSize = 10, split = [1,5])
        self.panel2 = DynamicLinePanel(
                noteLabels, noteValues,
                fontSize = 10,
                split = [1,5],
                lineMinHeight = 50,
                lineMaxHeight = 50
            )

        self.routineTab = RoutineTab(self.routineModel(), self.alternativeModel())
        self.evaluatorTab1 = EvaluatorTab(self.routineModel(), GraphicalEvaluator.GraphicalEvaluator())
        self.evaluatorTab2 = EvaluatorTab(self.alternativeModel(), GraphicalEvaluator.GraphicalEvaluator())
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.addTab(self.routineTab, "Trainingroutine")
        self.tabWidget.addTab(self.evaluatorTab1, "Evaluation: Trainingroutine")
        self.tabWidget.addTab(self.evaluatorTab2, "Evaluation: Trainingalternatives")

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addNoteButton = QtWidgets.QPushButton("+")
        self.deleteNoteButton = QtWidgets.QPushButton("-")
        self.buttonLayout.addWidget(self.addNoteButton)
        self.buttonLayout.addWidget(self.deleteNoteButton)

        self.mainLayout.addWidget(self.panel1, 0, 0)
        self.mainLayout.addWidget(self.panel2, 1, 0)
        self.mainLayout.addLayout(self.buttonLayout, 2, 0)
        self.mainLayout.addWidget(self.tabWidget, 0, 1, 3, 1)
        self.mainLayout.setRowStretch(1, 2)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 2)
        self.mainLayout.setSpacing(20)

        self.__connectButtons()

        self.showMaximized()

    def __connectButtons(self):
        self.addNoteButton.clicked.connect(self.addNote)
        self.deleteNoteButton.clicked.connect(self.deleteNote)

    def __calculateEndData(self, startDate):
        pattern = "(?P<day>\d\d).(?P<month>\d\d).(?P<year>\d\d\d\d)"
        match = re.search(pattern, startDate)
        year = int(match.group("year"))
        month = int(match.group("month"))
        day = int(match.group("day"))
        start = datetime.date(year, month, day)
        endDate = start + datetime.timedelta(days = 42)
        return endDate.strftime("%d.%m.%Y")

    def addNote(self, event):
        labels = self.panel2.labels()
        values = self.panel2.values()
        labels.append("None:")
        values.append("0123456789----- "*10)
        self.panel2.setLabels(labels)
        self.panel2.setValues(values)
        self.panel2.updatePanel()

    def alternativeModel(self):
        return self._alternativeModel


    def configParser(self):
        return self._configParser

    def database(self):
        return self._database

    def deleteNote(self, event):
        labels = self.panel2.labels()
        values = self.panel2.values()
        if len(labels) == 0 or len(values) == 0:
            return
        else:
            labels.pop()
            values.pop()
            self.panel2.setLabels(labels)
            self.panel2.setValues(values)
            self.panel2.updatePanel()

    def evaluator(self):
        return self._evaluator

    def exporter(self):
        return self._exporter

    def routineModel(self):
        return self._routineModel

    def setAlternativeModel(self, alternativeModel):
        if not isinstance(alternativeModel, CustomModel.CustomSqlModel) and alternativeModel is not None:
            raise TypeError(
                    "input <{input_name}> for 'alternativeModel' does not match {type_name}".format(
                            input_name = str(alternativeModel),
                            type_name = CustomModel.CustomSqlModel
                        )
                )
        self._alternativeModel = alternativeModel

    def setConfigParser(self, configParser):
        if not isinstance(configParser, ConfigInterface.ConfigParser) and configParser is not None:
            raise TypeError(
                    "input <{input_name}> for 'configParser' does not match {type_name}".format(
                            input_name = str(configParser),
                            type_name = ConfigInterface.ConfigParser
                        )
                )
        self._configParser = configParser

    def setDatabase(self, database):
        if not isinstance(database, str) and not isinstance(database, pathlib2.Path) and database is not None:
            raise TypeError(
                    "input <{input_name}> for 'database' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(database),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        self._database = database

    def setEvaluator(self, evaluator):
        if not isinstance(evaluator, GraphicalEvaluator.GraphicalEvaluator) and evaluator is not None:
            raise TypeError(
                    "input <{input_name}> for 'evaluator' does not match {type_name}".format(
                            input_name = str(evaluator),
                            type_name = GraphicalEvaluator.GraphicalEvaluator
                        )
                )
        self._evaluator = evaluator

    def setExporter(self, exporter):
        if not isinstance(exporter, Exporter.Exporter) and exporter is not None:
            raise TypeError(
                    "input <{input_name}> for 'exporter' does not match {type_name}".format(
                            input_name = str(exporter),
                            type_name = Exporter.Exporter
                        )
                )
        self._exporter = exporter

    def setRoutineModel(self, routineModel):
        if not isinstance(routineModel, CustomModel.CustomSqlModel) and routineModel is not None:
            raise TypeError(
                    "input <{input_name}> for 'routineModel' does not match {type_name}".format(
                            input_name = str(routineModel),
                            type_name = CustomModel.CustomSqlModel
                        )
                )
        self._routineModel = routineModel

class GridPanel(cc.CustomWidget):

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
                GridPanel {background-color: rgba(255,255,255,100%)}
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
            valueWidget.setFont(valueFont)

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

class DynamicLinePanel(cc.CustomWidget):

    def __init__(self, labels, values, *args,
                 fontSize = 8,
                 split = [1, 1],
                 lineMinHeight = 50,
                 lineMaxHeight = 200):

        super().__init__(*args)
        self._labels = None
        self._values = None
        self._fontSize = None
        self._widgets = None
        self._split = None
        self._lineMinHeight = None
        self._lineMaxHeight = None

        self._mainLayout = cc.CustomBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        self._mainLayout.setContentsMargins(0,0,0,0)
        self._mainWidget = None
        self._scrollArea = None

        self.setLabels(labels)
        self.setValues(values)
        self.setFontSize(fontSize)
        self.setSplit(split)
        self.setLineMinHeight(lineMinHeight)
        self.setLineMaxHeight(lineMaxHeight)
        self.setLayout(self._mainLayout)

        self.__createPanel()

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
                    "labels must have the same length as values"
                )
        self.__initiateWidgets()

        self._mainWidget = cc.CustomWidget()
        self._scrollArea = cc.CustomScrollArea(self._mainWidget)
        self._scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._mainLayout.addWidget(self._scrollArea)

        layout = cc.CustomBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        layout.setContentsMargins(0,0,0,0)

        for i,_ in enumerate(self.labels()):
            subLayout = cc.CustomBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
            subLayout.setSpacing(0)
            label = self.labels()[i]
            value = self.values()[i]

            labelString = label
            labelFont = QtGui.QFont()
            labelFont.setBold(True)
            labelFont.setPointSize(self.fontSize())
            labelWidget = QtWidgets.QLabel(labelString)
            labelWidget.setTextFormat(QtCore.Qt.RichText)
            labelWidget.setMargin(11)
            labelWidget.setFont(labelFont)
            labelWidget.setMinimumHeight(self.lineMinHeight())
            labelWidget.setMaximumHeight(self.lineMaxHeight())
            labelWidget.setStyleSheet(
                """
                QLabel {background-color: rgba(255,255,255,100%)}
                """
                )

            valueString = value
            valueFont = QtGui.QFont()
            valueFont.setPointSize(self.fontSize())
            valueWidget = QtWidgets.QLabel(valueString)
            valueWidget.setWordWrap(True)
            valueWidget.setTextFormat(QtCore.Qt.RichText)
            valueWidget.setMargin(11)
            valueWidget.setFont(valueFont)
            valueWidget.setMinimumHeight(self.lineMinHeight())
            valueWidget.setMaximumHeight(self.lineMaxHeight())
            valueWidget.setStyleSheet(
                """
                QLabel {background-color: rgba(255,255,255,100%)}
                """
                )

            subLayout.addWidget(labelWidget)
            subLayout.addWidget(valueWidget)

            self._widgets[i][0] = labelWidget
            self._widgets[i][1] = valueWidget

            layout.addLayout(subLayout)

        self.__calculateContentSplit()
        layout.addStretch(2)
        self._mainWidget.setLayout(layout)

    def __calculateContentSplit(self):
        frac1 = self.split()[0] / sum(self.split())
        frac2 = self.split()[1] / sum(self.split())
        width = self.width()
        for line in self._widgets:
            for i, widget in enumerate(line):
                if i == 0:
                    widget.setMaximumWidth(round(width*frac1))
                    widget.setMinimumWidth(round(width*frac1))
                if i == 1:
                    widget.setMaximumWidth(round(width*frac2))
                    widget.setMinimumWidth(round(width*frac2))

    def fontSize(self):
        return self._fontSize

    def labels(self):
        return self._labels

    def lineMaxHeight(self):
        return self._lineMaxHeight

    def lineMinHeight(self):
        return self._lineMinHeight

    def resizeEvent(self, event):
        self.__calculateContentSplit()
        super().resizeEvent(event)

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

    def setLineMaxHeight(self, maxh):
        if not isinstance(maxh, int):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
                            input_name = str(maxh),
                            type_name = int
                        )
                )
        if maxh < 0:
            raise ValueError(
                    "'maxh' has to be greater or equal than zero"
                )
        self._lineMaxHeight = maxh

    def setLineMinHeight(self, minh):
        if not isinstance(minh, int):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
                            input_name = str(minh),
                            type_name = int
                        )
                )
        if minh < 0:
            raise ValueError(
                    "'minh' has to be greater or equal than zero"
                )
        self._lineMinHeight = minh

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
        self._mainLayout.removeWidget(self._scrollArea)
        self._scrollArea.deleteLater()
        self.__createPanel()

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

    def __init__(self, routineModel, alternativeModel, *args):
        super().__init__(*args)
        self._routineModel = None
        self._alternativeModel = None
        self._headerLabels = None
        self._layout = None
        self._routineView = None
        self._alternativeView = None

        self.setRoutineModel(routineModel)
        self.setAlternativeModel(alternativeModel)

        self.setHeaderLabels([
                "Exercise",
                "Sets",
                "Reps",
                "Warm Up",
                "Week 1",
                "Week 2",
                "Week 3",
                "Week 4",
                "Week 5",
                "Week 6",
                "Mode"
            ])

        if self.routineModel() and self.alternativeModel():
            self.setLayout(cc.CustomBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self))
            self.setRoutineView(
                    CustomTableView.CustomModelView(
                            self.routineModel(),
                            headerLabels = self.headerLabels(),
                            fontSize = 15,
                            fontWeight = "normal",
                            fontStyle = "normal",
                            labelMode = "main",
                            parent = self
                        )
                )
            self.setAlternativeView(
                    CustomTableView.CustomModelView(
                            self.alternativeModel(),
                            headerLabels = self.headerLabels(),
                            fontSize = 15,
                            fontWeight = "normal",
                            fontStyle = "normal",
                            labelMode = "alternative",
                            parent = self
                        )
                )
            self.__harmonizeColumnWidths(self.alternativeView(), self.routineView())
            self.layout().addWidget(self.routineView())
            self.layout().addWidget(self.alternativeView())

    def __harmonizeColumnWidths(self, *args):
        newWidth = list()
        for table in args:
            header = table.horizontalHeader()
            width = list()
            for i in range(header.count()):
                width.append(header.sectionSize(i))
            width = max(width)
            newWidth.append(width)
        newWidth = max(newWidth)

        for table in args:
            header = table.horizontalHeader()
            table.setColumnWidth(0, newWidth)
            for i in range(header.count()):
                if i > 0:
                    table.resizeColumnToContents(i)

    def alternativeModel(self):
        return self._alternativeModel

    def alternativeView(self):
        return self._alternativeView

    def headerLabels(self):
        return self._headerLabels

    def layout(self):
        return self._layout

    def routineModel(self):
        return self._model

    def routineView(self):
        return self._routineView

    def setAlternativeModel(self, model):
        self._alternativeModel = model

    def setAlternativeView(self, view):
        self._alternativeView = view

    def setHeaderLabels(self, labels):
        self._headerLabels = labels

    def setLayout(self, layout):
        self._layout = layout

    def setRoutineModel(self, model):
        self._model = model

    def setRoutineView(self, view):
        self._routineView = view

class EvaluatorTab(cc.CustomWidget):

    def __init__(self, model, graphicalEvaluator, *args):
        super().__init__(*args)
        self._model = None
        self._evaluator = None

        self.setModel(model)
        self.setEvaluator(graphicalEvaluator)

        if self.evaluator() and self.model():
            self.evaluator().connectEvaluator(self)
            self.evaluator().setModel(self.model())
            self.evaluator().initiateQWidgets()
            self.evaluator().createTabs(self.evaluator().dataFromModel())
            self.evaluator().plotData(self.evaluator().dataFromModel())

    def evaluator(self):
        return self._evaluator

    def model(self):
        return self._model

    def setEvaluator(self, evaluator):
        self._evaluator = evaluator

    def setModel(self, model):
        self._model = model

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())