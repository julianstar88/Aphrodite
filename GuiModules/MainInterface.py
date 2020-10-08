# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:58:37 2020

@author: Julian
"""

import re
import os
import pathlib
import datetime
import shutil
from PyQt5 import QtWidgets, QtCore, QtGui

from MainModules import ConfigInterface, Database, Exporter, GraphicalEvaluator
from UtilityModules import CustomModel
from GuiModules import CustomTableView, ProgressDialog
import GuiModules.CustomGuiComponents as cc


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, configParser, *args):

        super().__init__(*args)

        """initialize private properties (Main-Objects)"""
        self._configParser = None
        self._database = None
        self._evaluator = None
        self._exporter = None
        self._alternativeModel = None
        self._routineModel = None

        """initialize public properties"""
        self.panel1 = None
        self.panel2 = None
        self.routineTab = None
        self.evaluatorTab1 = None
        self.evaluatorTab2 = None
        self.tabWidget = None
        self.buttonLayout = None
        self.addNoteButton = None
        self.deleteNoteButton = None

        """process input parameter"""
        self.setConfigParser(configParser)
        self.populateMainObjects("last_opened_routine")

        """general settings for app"""
        self.setWindowTitle("Aphrodite")
        self.mainWidget = cc.CustomWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.setGeometry(50,200,1600,500)
        self.setCentralWidget(self.mainWidget)
        self.setWindowIcon(cc.CustomIcon(iconPath = "files/icons/app_icons"))

        """populate app app"""
        self.openRoutine()

        """show the app"""
        self.showMaximized()
        # self.show()

        """update widget geometries"""
        self.updateWindow()

    def __connectButtons(self):
        self.editAlternativesButton.clicked.connect(self.onEditAlternatives)
        self.editNotesButton.clicked.connect(self.onEditNotes)
        self.editRoutineButton.clicked.connect(self.onEditRoutine)

    def __calculateEndData(self, startDate):
        pattern = "(?P<day>\d\d).(?P<month>\d\d).(?P<year>\d\d\d\d)"
        match = re.search(pattern, startDate)
        year = int(match.group("year"))
        month = int(match.group("month"))
        day = int(match.group("day"))
        start = datetime.date(year, month, day)
        endDate = start + datetime.timedelta(days = 42)
        return endDate.strftime("%d.%m.%Y")

    def __createMenuBar(self):

        try:
            self.menu.clear()
        except:
            pass

        """top level menus"""
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&File")
        self.editMenu = self.menu.addMenu("&Edit")
        self.helpMenu = self.menu.addMenu("&Help")

        """1. level menus"""
        folderIcon = QtGui.QIcon("files/icons/black_folder.png")
        diskIcon = QtGui.QIcon("files/icons/black_disk.png")
        sheetIcon = QtGui.QIcon("files/icons/sheet.png")
        pencilIcon = QtGui.QIcon("files/icons/pencil.png")
        infoIcon = QtGui.QIcon("files/icons/info.png")
        quitIcon = QtGui.QIcon("files/icons/quit.png")
        exportIcon = QtGui.QIcon("files/icons/export.png")

        self.newRoutineAction = self.fileMenu.addAction(folderIcon, "&New Trainingroutine...")
        self.fileMenu.addSeparator()
        self.openRoutineAction = self.fileMenu.addAction(sheetIcon, "&Open Trainingroutine...")
        self.openLastClosedAction = self.fileMenu.addAction("O&pen last closed")
        self.fileMenu.addSeparator()
        self.saveAsAction = self.fileMenu.addAction(diskIcon, "&Save As...")
        self.fileMenu.addSeparator()
        self.exportAction = self.fileMenu.addAction(exportIcon, "&Export Trainingroutine...")
        self.fileMenu.addSeparator()
        self.quitAction = self.fileMenu.addAction(quitIcon, "&Quit")

        self.editRoutineAction = self.editMenu.addAction(pencilIcon, "&Edit Trainingroutine...")
        self.editAlternativesAction = self.editMenu.addAction("Edit Training&alternatives...")
        self.editNotesAction = self.editMenu.addAction("Edit Training&notes...")
        self.editMenu.addSeparator()

        self.aboutAphroditeAction = self.helpMenu.addAction(infoIcon, "&About Aphrodite...")

        # connections
        self.newRoutineAction.triggered.connect(self.onCreateNewRoutine)
        self.openRoutineAction.triggered.connect(self.onOpenTrainingroutine)
        self.openLastClosedAction.triggered.connect(self.onOpenLastClosed)
        self.saveAsAction.triggered.connect(self.onSaveAs)
        self.exportAction.triggered.connect(self.onExportTrainingroutine)
        self.quitAction.triggered.connect(self.onDestroyed)

        self.editAlternativesAction.triggered.connect(self.onEditAlternatives)
        self.editNotesAction.triggered.connect(self.onEditNotes)
        self.editRoutineAction.triggered.connect(self.onEditRoutine)

        self.aboutAphroditeAction.triggered.connect(self.onAboutAphrodite)

        if self.database().isValid():
            self.quitAction.setEnabled(True)
            self.editRoutineAction.setEnabled(True)
            self.editAlternativesAction.setEnabled(True)
            self.editNotesAction.setEnabled(True)
            self.exportAction.setEnabled(True)
            self.saveAsAction.setEnabled(True)
            self.quitAction.setEnabled(True)
        else:
            self.quitAction.setEnabled(False)
            self.editRoutineAction.setEnabled(False)
            self.editAlternativesAction.setEnabled(False)
            self.editNotesAction.setEnabled(False)
            self.exportAction.setEnabled(False)
            self.saveAsAction.setEnabled(False)
            self.quitAction.setEnabled(False)

    def alternativeModel(self):
        return self._alternativeModel

    def closeEvent(self, event):
        self.onDestroyed()

    def closeRoutine(self):

        # delete all widgets
        self.setWindowTitle("Aphrodite")
        def deleteTabWidget(widget):
            for i in range(widget.count()):
                children = widget.widget(i).children()
                childrenTypes = [type(element) for element in children]
                childWidget = widget.widget(i)
                if QtWidgets.QTabWidget in childrenTypes:
                    childWidget.evaluator().clearTabs()
            widget.deleteLater()

        for i in reversed(range(self.mainLayout.count())):
            child = self.mainLayout.itemAt(i)
            if child.widget():
                if not isinstance(child.widget(), QtWidgets.QTabWidget):
                    child.widget().deleteLater()
                else:
                    deleteTabWidget(child.widget())
            else:
                for n in reversed(range(child.count())):
                    grandChild = child.takeAt(n)
                    grandChild.widget().deleteLater()

        # write recently closed database to the configFile
        try:
            file = self.database().path() / (self.database().databaseName() + self.database().extension())
            self.configParser().last_closed_routine = str(file)
            self.configParser().writeConfigFile()
        except TypeError:
            pass

    def configParser(self):
        return self._configParser

    def database(self):
        return self._database

    def evaluator(self):
        return self._evaluator

    def exporter(self):
        return self._exporter

    def initiateMainObjects(self):
        self.configParser().readConfigFile()

    def onAboutAphrodite(self):
        msg = """
            <p style='text-align:center'>
            <b>Aphrodite</b><br>
            v.x.x.x
            </p>

            <p style='text-align:center'>
            <img style='text-align:center' src='files/icons/app_icons/About_Aphrodite.png'>
            </p>

            <p style='text-align:center'>
            <b>Aphrodite is a programm to create Training routines.</b><br>
            Copyright (C) 2020 Julian Blaser<br>
            Email: <a href=mailto:milits-julian@web.de>milites-julian@web.de</a>
            </p>

            <p style='text-align:center'>
            This programm is free software: you can resistribute it and/ or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.
            </p>

            <p style='text-align:center'>
            This program is distributed in the hope that it will be usefule,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
            GNU General Public License for more details.
            </p>

            <p style='text-align:center'>
            You should have received a copy of the GNU General Public License
            along with this programm. If not, see <a href="https://www.gnu.org/licenses/">GNU GPL</a>.
            </p>
        """
        messageBox = cc.CustomMessageBox(msg)
        messageBox.setTextFormat(QtCore.Qt.RichText)
        messageBox.setIcon(QtWidgets.QMessageBox.NoIcon)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        messageBox.setWindowTitle("About Aphrodite")
        messageBox.exec()

    def onCreateNewRoutine(self, *args):
        dialog = cc.CustomCreateNewRoutineDialog(
                self.configParser(),
                parent = self
            )
        if dialog.result():
            databaseName = dialog.toCommit()["databaseName"]
            general_information = dialog.toCommit()["general_information"]
            new_routine_directory = dialog.toCommit()["new_routine_directory"]

            file = pathlib.Path(new_routine_directory) / pathlib.Path(databaseName + self.database().extension())

            if file.is_file():
                message = "The file '{filename}' already exists. Do you want to replace it?".format(
                        filename = databaseName + self.database().extension()
                    )
                messageBox = cc.CustomMessageBox(
                    message,
                    windowTitle = "Export Trainingroutine",
                    )
                messageBox.exec()
                if messageBox.result() == QtWidgets.QMessageBox.Ok:
                    pass
                if messageBox.result() == QtWidgets.QMessageBox.Cancel:
                    return False


            self.database().setPath(new_routine_directory)
            self.database().setDatabaseName(databaseName)
            self.database().createDatabase()
            self.database().createRoutineTables()

            self.database().setGeneralInformation(
                    general_information[0],
                    general_information[1],
                    general_information[2]
                )

            # file = self.database().path() / (self.database().databaseName() + self.database().extension())
            self.configParser().new_routine_directory = new_routine_directory
            self.configParser().last_opened_routine = str(file)
            self.configParser().writeConfigFile()

            self.populateMainObjects("last_opened_routine")
            self.closeRoutine()
            self.openRoutine()
            return True
        else:
            return False

    def onDestroyed(self, *args):
        self.closeRoutine()
        self.deleteLater()

    def onEditAlternatives(self, *args):
        dialog = cc.CustomEditAlternativesDialog(
                self.database(),
                parent = self
            )
        if dialog.result():
            if not self.database().isValid():
                return False

            self.database().deleteAllEntries("training_alternatives")
            self.database().addManyEntries("training_alternatives", dialog.toCommit())
            self.updateWindow()
            return True
        else:
            return False


    def onEditNotes(self, *args):
        dialog = cc.CustomEditNotesDialog(
                self.database(),
                parent = None
            )
        if dialog.result():
            if not self.database().isValid():
                return False
            self.database().deleteAllEntries("training_notes")
            self.database().addManyEntries("training_notes", dialog.toCommit())
            self.updateWindow()
            return True
        else:
            return False

    def onEditRoutine(self, *args):
        dialog = cc.CustomEditRoutineDialog(
                self.database(),
                parent = self,
            )
        if dialog.result():
            if not self.database().isValid():
                return False

            for key in dialog.toCommit().keys():
                self.database().deleteAllEntries(key)
                self.database().addManyEntries(key, dialog.toCommit()[key])
            self.updateWindow()
            return True
        else:
            return False

    def onExportTrainingroutine(self):

        # collect export path
        progress = ProgressDialog.ProgressWindow(self)
        progress.hide()
        dialog = QtWidgets.QFileDialog()
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setNameFilter("Excel (*.xlsx)")
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        exportDirStr = self.configParser().export_routine_directory
        defaultName = self.database().databaseName()
        if exportDirStr:
            exportDir = pathlib.Path(exportDirStr)
        else:
            exportDir = pathlib.Path(__file__).cwd() / pathlib.Path("training_routines")

        dialog.setDirectory(str(exportDir))
        dialog.selectFile(defaultName)

        if dialog.exec():
            file = pathlib.Path(dialog.selectedFiles()[0])
            data = self.database().data("general_information")
            path = file.parent
            routineName = file.name

            if file.is_file():
                message = "The file '{filename}' already exists. Do you want to replace it?".format(
                        filename = routineName
                    )
                messageBox = cc.CustomMessageBox(
                    message,
                    windowTitle = "Export Trainingroutine",
                    )
                messageBox.exec()
                if messageBox.result() == QtWidgets.QMessageBox.Ok:
                    pass
                if messageBox.result() == QtWidgets.QMessageBox.Cancel:
                    return False

            try:
                userName = data[0][0]
            except:
                userName = "None"
            try:
                startDateStr = data[0][1]
            except:
                date = datetime.date.today()
                startDateStr = date.strftime("%d.%m.%Y")
            try:
                trainingMode = data[0][2]
                if len(trainingMode) == 0:
                    trainingMode = "None"
            except:
                trainingMode = "None"

            match = re.search("(?P<d>\d+).(?P<m>\d+).(?P<y>\d+)", startDateStr)

            self.configParser().export_routine_directory = path
            self.configParser().writeConfigFile()
            
            progress.show()
            self.exporter().setExportPath(str(path))
            self.exporter().setDatabase(
                    self.database().path() / (self.database().databaseName() + self.database().extension())
                )
            self.exporter().setRoutineName(routineName)
            self.exporter().setName(userName)
            self.exporter().setTrainingMode(trainingMode)
            self.exporter().setTrainingPeriode(
                    int(match.group("y")), int(match.group("m")), int(match.group("d"))
                )
            self.exporter().export()
            progress.deleteLater()

            return True

        return False

    def onOpenLastClosed(self, *args):
        # collect database name of last closed database
        lastClosedFileStr = self.configParser().last_closed_routine

        #  provide database name to database and open the new trainingroutine
        self.database().setPath(lastClosedFileStr)
        self.closeRoutine()
        self.populateMainObjects("last_closed_routine")
        self.openRoutine()
        self.updateWindow()

    def onOpenTrainingroutine(self, *args):
        # collect database name
        dialog = QtWidgets.QFileDialog()
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setNameFilter("database (*.db)")
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        lastOpenedFileStr = self.configParser().last_opened_routine
        if lastOpenedFileStr:
            lastOpenedFile = pathlib.Path(lastOpenedFileStr)
            lastOpenedDir = lastOpenedFile.parent
            dialog.selectFile(lastOpenedFile.name)
        else:
            lastOpenedDir = pathlib.Path(__file__).cwd() / pathlib.Path("training_routines")

        dialog.setDirectory(str(lastOpenedDir))
        if (dialog.exec()):
            file = pathlib.Path(dialog.selectedFiles()[0])
            if (file.is_file()):
                self.closeRoutine()
                self.configParser().last_opened_routine = str(file)
                self.configParser().writeConfigFile()

                # provide database name to database and open the new trainingroutine
                self.database().setPath(file)
                self.populateMainObjects("last_opened_routine")
                self.openRoutine()
                self.updateWindow()

    def onSaveAs(self, *args):

        # collect path to save copy
        dialog = QtWidgets.QFileDialog()
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setNameFilter("database (*.db)")
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dialog.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite)

        # set default directory
        lastOpenedFileStr = self.configParser().last_opened_routine
        if lastOpenedFileStr:
            lastOpenedFile = pathlib.Path(lastOpenedFileStr)
            lastOpenedDir = lastOpenedFile.parent
        else:
            lastOpenedDir = pathlib.Path(__file__).cwd() / pathlib.Path("training_routines")
        dialog.setDirectory(str(lastOpenedDir))

        # guess a default file name
        date = datetime.date.today()
        strDate = date.strftime("%y%m%d")
        fileNameProposal = "Training-{}".format(strDate)
        files = [s for s in os.listdir(lastOpenedDir) if s.endswith(".db")]
        nameCount = 1
        for file in files:
            if re.search(fileNameProposal, file):
                nameCount += 1
        if nameCount > 1:
            fileNameProposal = "{old_proposal}({num})".format(
                    old_proposal = fileNameProposal,
                    num = nameCount
                )
        dialog.selectFile(fileNameProposal)

        # execute dialog
        if dialog.exec():
            pass
            newFile = pathlib.Path(dialog.selectedFiles()[0])
            shutil.copy2(lastOpenedFile, newFile)

    def openRoutine(self, *args):
        generalLabels = ["Name:", "Start:", "End:", "Trainingmode:"]
        generalValues = ["None", "None", "None", "None"]
        noteLabels = []
        noteValues = []

        self.__createMenuBar()

        if self.database().isValid():
            data = self.database().data("general_information")[0]
            generalValues = [data[0], data[1], self.__calculateEndData(data[1]), data[2]]

            data = self.database().data("training_notes")
            noteLabels = list()
            noteValues = list()
            for note in data:
                noteLabels.append(note[1])
                noteValues.append(note[3])

            self.setWindowTitle("Aphrodite: " + self.database().databaseName())
            self.panel1 = GridPanel(
                    generalLabels,
                    generalValues,
                    fontSize = None,
                    split = [1,5]
                )
            self.panel2 = DynamicLinePanel(
                    noteLabels, noteValues,
                    fontSize = None,
                    split = [1,5],
                    lineMinHeight = 55,
                    lineMaxHeight = 55
                )

            self.routineTab = RoutineTab(self.routineModel(), self.alternativeModel(), self.database())

            self.evaluatorTab1 = EvaluatorTab(self.routineModel(), GraphicalEvaluator.GraphicalEvaluator())
            self.evaluatorTab2 = EvaluatorTab(self.alternativeModel(), GraphicalEvaluator.GraphicalEvaluator())

            self.tabWidget = QtWidgets.QTabWidget()
            self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
            self.tabWidget.addTab(self.routineTab, "Trainingroutine")
            self.tabWidget.addTab(self.evaluatorTab1, "Evaluation: Trainingroutine")
            self.tabWidget.addTab(self.evaluatorTab2, "Evaluation: Trainingalternatives")
            self.tabWidget.tabBarClicked.connect(self.evaluatorTab1.onTabBarClicked)
            self.tabWidget.tabBarClicked.connect(self.evaluatorTab2.onTabBarClicked)

            self.buttonLayout = QtWidgets.QHBoxLayout()
            self.editAlternativesButton = QtWidgets.QPushButton("Edit Alternatives...")
            self.editNotesButton = QtWidgets.QPushButton("Edit Notes...")
            self.editRoutineButton = QtWidgets.QPushButton("Edit Routine...")
            self.buttonLayout.addWidget(self.editAlternativesButton)
            self.buttonLayout.addWidget(self.editNotesButton)
            self.buttonLayout.addWidget(self.editRoutineButton)

            self.__connectButtons()

            self.mainLayout.addWidget(self.panel1, 0, 0)
            self.mainLayout.addWidget(self.panel2, 1, 0)
            self.mainLayout.addLayout(self.buttonLayout, 2, 0)
            self.mainLayout.addWidget(self.tabWidget, 0, 1, 3, 1)
            self.mainLayout.setRowStretch(1, 2)
            self.mainLayout.setColumnStretch(0, 1)
            self.mainLayout.setColumnStretch(1, 3)
            self.mainLayout.setSpacing(5)

            self.__createMenuBar()

        else:
            self.setWindowTitle("Aphrodite")

    def populateMainObjects(self, attr):
        path = pathlib.Path(self.configParser().readAttributes()[attr])
        if self.database() is None:
            database = Database.database(path)
            self.setDatabase(database)
        else:
            self.database().setPath(path)

        if self.database().isValid():
            trainingModel = CustomModel.CustomSqlModel(
                    database = self.database(),
                    table = "training_routine",
                    tableStartIndex = 0,
                    valueStartIndex = 1
                )
            trainingModel.populateModel()
            self.setRoutineModel(trainingModel)

            alternativeModel = CustomModel.CustomSqlModel(
                    database = self.database(),
                    table = "training_alternatives",
                    tableStartIndex = 3,
                    valueStartIndex = 1
                )
            alternativeModel.populateModel()
            self.setAlternativeModel(alternativeModel)

            file = self.database().path() / (self.database().databaseName() + self.database().extension())
            exporter = Exporter.Exporter()
            exporter.setDatabase(file)
            self.setExporter(exporter)

            evaluator = GraphicalEvaluator.GraphicalEvaluator()
            evaluator.setDatabase(
                    self.database().path() / (self.database().databaseName() + self.database().extension())
                )
            self.setEvaluator(evaluator)

            return True
        else:
            return False

    def routineModel(self):
        return self._routineModel

    def setAlternativeModel(self, alternativeModel):
        if not isinstance(alternativeModel, CustomModel.CustomSqlModel) and alternativeModel is not None:
            raise TypeError(
                    "input <{input_name}> for 'alternativeModel' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(alternativeModel),
                            type_name_1 = CustomModel.CustomSqlModel,
                            type_name_2 = None
                        )
                )
        self._alternativeModel = alternativeModel

    def setConfigParser(self, configParser):
        if not isinstance(configParser, ConfigInterface.ConfigParser) and configParser is not None:
            raise TypeError(
                    "input <{input_name}> for 'configParser' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(configParser),
                            type_name_1 = ConfigInterface.ConfigParser,
                            type_name_2 = None
                        )
                )
        self._configParser = configParser

    def setDatabase(self, database):
        if not isinstance(database, Database.database) and database is not None:
            raise TypeError(
                    "input <{input_name}> for 'database' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(database),
                            type_name_1 = pathlib.Path,
                            type_name_2 = None
                        )
                )
        self._database = database

    def setEvaluator(self, evaluator):
        if not isinstance(evaluator, GraphicalEvaluator.GraphicalEvaluator) and evaluator is not None:
            raise TypeError(
                    "input <{input_name}> for 'evaluator' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(evaluator),
                            type_name_1 = GraphicalEvaluator.GraphicalEvaluator,
                            type_name_2 = None
                        )
                )
        self._evaluator = evaluator

    def setExporter(self, exporter):
        if not isinstance(exporter, Exporter.Exporter) and exporter is not None:
            raise TypeError(
                    "input <{input_name}> for 'exporter' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(exporter),
                            type_name_1 = Exporter.Exporter,
                            type_name_2 = None
                        )
                )
        self._exporter = exporter

    def setRoutineModel(self, routineModel):
        if not isinstance(routineModel, CustomModel.CustomSqlModel) and routineModel is not None:
            raise TypeError(
                    "input <{input_name}> for 'routineModel' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(routineModel),
                            type_name_1 = CustomModel.CustomSqlModel,
                            type_name_2 = None
                        )
                )
        self._routineModel = routineModel

    def updateWindow(self, *args):
        if self.database().isValid():
            data = self.database().data("general_information")[0]
            generalValues = [data[0], data[1], self.__calculateEndData(data[1]), data[2]]

            data = self.database().data("training_notes")
            noteLabels = list()
            noteValues = list()
            for note in data:
                if note[0] is not None:
                    noteLabels.append(note[1])
                else:
                    noteLabels.append("")
                noteValues.append(note[3])

        try:
            self.panel1.setValues(generalValues)
            self.panel1.updatePanel()
        except AttributeError: # generalValues is not valid
            pass

        try:
            self.panel2.setLabels(noteLabels)
            self.panel2.setValues(noteValues)
            self.panel2.updatePanel()
        except AttributeError: # notelabels and/ or noteValues are not valid
            pass

        try:
            self.routineTab.updatePanel()
        except AttributeError: # no valid panels to update
            pass

        try:
            self.evaluatorTab1.updatePanel()
            self.evaluatorTab2.updatePanel()
        except AttributeError: # no valid panels to update
            pass

        try:
            self.repaint()
            self.menu.repaint()
            self.tabWidget.repaint()
        except AttributeError: # no valid panels to repaint
            pass

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

            labelWidget, valueWidget = self.panelLineContent(label, value)

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

    def panelLineContent(self, label, value):
            labelString = label
            labelFont = QtGui.QFont()
            labelFont.setBold(True)
            if self.fontSize():
                labelFont.setPointSize(self.fontSize())

            labelWidget = QtWidgets.QLabel(labelString)
            labelWidget.setTextFormat(QtCore.Qt.RichText)
            labelWidget.setFont(labelFont)

            valueString = value
            valueFont = QtGui.QFont()
            if self.fontSize():
                valueFont.setPointSize(self.fontSize())

            valueWidget = QtWidgets.QLabel(valueString)
            valueWidget.setTextFormat(QtCore.Qt.RichText)
            valueWidget.setFont(valueFont)

            return labelWidget, valueWidget

    def setFontSize(self, size):
        if (not isinstance(size, int)) and (size is not None):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(size),
                            type_name_1 = int,
                            type_name_2 = None
                        )
                )
        try:
            if size < 0:
                raise ValueError(
                        "input <{input_name}> has to be greater than zero or {type_name}".format(
                                input_name = str(size),
                                type_name = None
                            )
                    )
        except TypeError: # if size is eg. None
            pass

        self._fontSize = size

    def setLabels(self, labels):
        if not isinstance(labels, list):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
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


            labelWidget, valueWidget = self.panelLineContent(label, value)

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

            if len(label) != 0:
                labelString = label + ")"
            else:
                labelString = ""
            labelFont = QtGui.QFont()
            labelFont.setBold(True)
            if self.fontSize():
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
            if self.fontSize():
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
        if (not isinstance(size, int)) and (size is not None):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(size),
                            type_name_1 = int,
                            type_name_2 = None
                        )
                )

        try:
            if size < 0:
                raise ValueError(
                        "MainInterface.Panel.setFontSize: input <{input_name}> has to be greater than zero".format(
                                input_name = str(size)
                            )
                    )
        except TypeError: # if size is eg. None
            pass

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

    def __init__(self, routineModel, alternativeModel, database, *args):
        super().__init__(*args)
        self._database = None
        self._routineModel = None
        self._alternativeModel = None
        self._alternativeScrollArea = None
        self._routineHeaderLabels = None
        self._alternativeHeaderLabels = None
        self._layout = None
        self._routineView = None
        self._routineScrollArea = None
        self._alternativeView = None

        self.setDatabase(database)
        self.setRoutineModel(routineModel)
        self.setAlternativeModel(alternativeModel)

        self.setRoutineHeaderLabels([
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

        self.setAlternativeHeaderLabels([
                "Alternative",
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


        self.createContent()
        self.routineModel().itemChanged.connect(self.displaySumOfSets)
        self.alternativeModel().itemChanged.connect(self.displaySumOfSets)

    def __harmonizeColumnWidths(self, *args):
        newWidth = list()
        for table in args:
            header = table.horizontalHeader()
            width = list()
            for i in range(header.count()):
                width.append(header.sectionSize(i))

            try:
                width = max(width)
            except ValueError:
                width = 0

            newWidth.append(width)

        newWidth = max(newWidth)

        for table in args:
            header = table.horizontalHeader()
            table.setColumnWidth(0, newWidth)
            for i in range(header.count()):
                if i > 0:
                    table.resizeColumnToContents(i)
        return True

    def alternativeHeaderLabels(self):
        return self._alternativeHeaderLabels

    def alternativeModel(self):
        return self._alternativeModel

    def alternativeScrollArea(self):
        return self._alternativeScrollArea

    def alternativeView(self):
        return self._alternativeView

    def createContent(self):
        if self.routineModel() and self.alternativeModel():
            self.setLayout(cc.CustomBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self))

            self.setRoutineView(
                    CustomTableView.CustomModelView(
                            self.routineModel(),
                            self,
                            headerLabels = self.routineHeaderLabels(),
                            headerFontSize = 15,
                            headerFontWeight = "normal",
                            headerFontStyle = "normal",
                            labelFontSize = 10,
                            labelFontStyle = "normal",
                            labelFontWeight = "normal",
                            labelMargin = 2,
                            labelMode = "main",
                            exerciseNameColumn = 0,
                            viewParent = self.routineScrollArea()
                        )
                )
            self.setAlternativeView(
                    CustomTableView.CustomModelView(
                            self.alternativeModel(),
                            self,
                            headerLabels = self.alternativeHeaderLabels(),
                            headerFontSize = 15,
                            headerFontWeight = "normal",
                            headerFontStyle = "normal",
                            labelFontSize = 10,
                            labelFontStyle = "normal",
                            labelFontWeight = "normal",
                            labelMargin = 2,
                            labelMode = "alternative",
                            exerciseNameColumn = 0,
                            viewParent = self.alternativeScrollArea()
                        )
                )
            self.__harmonizeColumnWidths(self.alternativeView(), self.routineView())

            self.setRoutineScrollArea(cc.CustomScrollArea(self.routineView()))
            self.setAlternativeScrollArea(cc.CustomScrollArea(self.alternativeView()))

            self.routineScrollArea().setFrameShape(QtWidgets.QFrame.NoFrame)
            self.alternativeScrollArea().setFrameShape(QtWidgets.QFrame.NoFrame)

            self.layout().addWidget(self.routineScrollArea())
            self.layout().addWidget(self.alternativeScrollArea())

    def database(self):
        return self._database

    def displaySumOfSets(self, item, role, defaultPurpose):

        setLimit = 30
        tipText = str()

        try:
            item.model()
        except RuntimeError:
            return False

        # exerciseSetItem will be used to display the sum of sets in the Tooltip
        if not item.model().horizontalHeaderItem(1):
            exerciseSetItem = QtGui.QStandardItem()
            item.model().setHorizontalHeaderItem(1, exerciseSetItem)

        sumOfSets = self.sumOfSets(item.model())

        if sumOfSets <= setLimit:
            color = "black"
        else:
            color = "firebrick"

        tipText = """
            <p style='text-align:center'>
            Number of Sets:
            </p>
            <p style='text-align:center'>
            <b style='color:{color}'>{num}</b> / <b style='color:black'>{limit}</b>
            </p>
        """.format(num = sumOfSets, color = color, limit = setLimit)
        item.model().horizontalHeaderItem(1).setToolTip(tipText)

        return True

    def layout(self):
        return self._layout

    def resizeEvent(self, event):
        self.__harmonizeColumnWidths(self.alternativeView(), self.routineView())
        super().resizeEvent(event)

    def routineHeaderLabels(self):
        return self._routineHeaderLabels

    def routineModel(self):
        return self._model

    def routineScrollArea(self):
        return self._routineScrollArea

    def routineView(self):
        return self._routineView

    def setAlternativeHeaderLabels(self, labels):
        if not isinstance(labels, list):
            raise TypeError(
                    "input <{input_name}> for 'setAlternativeHeaderLabels' does not match {type_name}".format(
                            input_name = str(labels),
                            type_name = list
                        )
                )
        for val in labels:
            if not isinstance(val, str):
                raise TypeError(
                        "element <{element}> in 'labels' for 'setAlternativeHeaderLabels' does not match {type_name}".format(
                                element = val,
                                type_name = str
                            )
                    )
        self._alternativeHeaderLabels = labels

    def setAlternativeModel(self, model):
        if not isinstance(model, CustomModel.CustomSqlModel) and model is not None:
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(model),
                            type_name_1 = CustomModel.CustomSqlModel,
                            type_name_2 = None
                        )
                )
        self._alternativeModel = model

    def setAlternativeScrollArea(self, scrollArea):
        if not isinstance(scrollArea, QtWidgets.QScrollArea):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
                            input_name = str(scrollArea),
                            type_name = QtWidgets.QScrollArea
                        )
                )
        self._alternativeScrollArea = scrollArea

    def setAlternativeView(self, view):
        if not isinstance(view, CustomTableView.CustomModelView):
            raise TypeError(
                    "input <{input_name}> for 'setAlternativeView' does not match {type_name}".format(
                            input_name = str(view),
                            type_name = CustomTableView.CustomModelView
                        )
                )
        view.keyReleased.connect(self.updateAlternativeTable)
        view.leftClicked.connect(self.updateAlternativeTable)
        view.leftDoubleClicked.connect(self.updateAlternativeTable)
        self._alternativeView = view

    def setDatabase(self, database):
        if not isinstance(database, Database.database) and database is not None:
            raise TypeError(
                    "input {input_name} for 'setDatabase' does not match {input_type}".format(
                            input_name = str(type(database)),
                            input_type = Database.database
                        )
                )
        self._database = database

    def setLayout(self, layout):
        if not isinstance(layout, QtWidgets.QBoxLayout):
            raise TypeError(
                    "input <{input_name}> for 'setLayout' does not match {type_name}".format(
                            input_name = str(layout),
                            type_name = QtWidgets.QBoxLayout
                        )
                )
        self._layout = layout

    def setRoutineHeaderLabels(self, labels):
        if not isinstance(labels, list):
            raise TypeError(
                    "input <{input_name}> for 'setRoutineHeaderLabels' does not match {type_name}".format(
                            input_name = str(labels),
                            type_name = list
                        )
                )
        for val in labels:
            if not isinstance(val, str):
                raise TypeError(
                        "element <{element}> in 'labels' for 'setRoutineHeaderLabels' does not match {type_name}".format(
                                element = val,
                                type_name = str
                            )
                    )
        self._routineHeaderLabels = labels

    def setRoutineModel(self, model):
        if not isinstance(model, CustomModel.CustomSqlModel) and model is not None:
            raise TypeError(
                    "input <{input_name}> for 'setRoutineModel' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(model),
                            type_name_1 = CustomModel.CustomSqlModel,
                            type_name_2 = None
                        )
                )
        self._model = model

    def setRoutineScrollArea(self, scrollArea):
        if not isinstance(scrollArea, QtWidgets.QScrollArea):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
                            input_name = str(scrollArea),
                            type_name = QtWidgets.QScrollArea
                        )
                )
        self._routineScrollArea = scrollArea

    def setRoutineView(self, view):
        if not isinstance(view, CustomTableView.CustomModelView):
            raise TypeError(
                    "input <{input_name}> for 'setRoutineView' does not match {type_name}".format(
                            input_name = str(view),
                            type_name = CustomTableView.CustomModelView
                        )
                )
        view.keyReleased.connect(self.updateRoutineTable)
        view.leftClicked.connect(self.updateRoutineTable)
        view.leftDoubleClicked.connect(self.updateRoutineTable)
        self._routineView = view

    def sumOfSets(self, model):
        rows = model.rowCount()
        sumOfSets = 0

        if rows > 0:
            for i in range(rows):
                sets = model.item(i, 1).userData()
                try:
                    sets = round(float(sets))
                except:
                    sets = 0
                sumOfSets += sets

        return sumOfSets

    def updatePanel(self):
        routineModel = self.routineView().model()
        alternativeModel = self.alternativeView().model()

        for n in range(routineModel.rowCount(), -1, -1):
            routineModel.removeRow(n)
        routineModel.populateModel()
        self.routineView().updateView()

        for n in range(alternativeModel.rowCount(), -1, -1):
            alternativeModel.removeRow(n)
        alternativeModel.populateModel()
        self.alternativeView().updateView()

        self.__harmonizeColumnWidths(self.alternativeView(), self.routineView())

    """slots"""
    def updateAlternativeTable(self, tableView, *args):
        modelData = list()
        for i in range(tableView.model().rowCount()):
            rowData = [tableView.model().item(i, col).userData() for col in range(tableView.model().columnCount())]
            modelData.append(rowData)

        tableData = self.database().data("training_alternatives")

        for i, row in enumerate(tableData):
            row[3:] = modelData[i]
            tableData[i] = row

        self.database().deleteAllEntries("training_alternatives")
        self.database().addManyEntries("training_alternatives", tableData)

    def updateRoutineTable(self, tableView, *args):
        modelData = list()
        for i in range(tableView.model().rowCount()):
            rowData = [tableView.model().item(i, col).userData() for col in range(tableView.model().columnCount())]
            modelData.append(rowData)

        self.database().deleteAllEntries("training_routine")
        self.database().addManyEntries("training_routine", modelData)

class EvaluatorTab(cc.CustomWidget):

    def __init__(self, model, graphicalEvaluator, *args):
        super().__init__(*args)
        self._model = None
        self._evaluator = None
        self._mainWindow = None
        self._progressWindow = None

        self.setModel(model)
        self.setEvaluator(graphicalEvaluator)

        self.createContent()

    def createContent(self):
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
        if not isinstance(evaluator, GraphicalEvaluator.GraphicalEvaluator) and evaluator is not None:
            raise TypeError(
                    "input <{input_name}> for 'setEvaluator' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(evaluator),
                            type_name_1 = GraphicalEvaluator.GraphicalEvaluator,
                            type_name_2 = None
                        )
                )
        self._evaluator = evaluator

    def setModel(self, model):
        if not isinstance(model, CustomModel.CustomSqlModel) and model is not None:
            raise TypeError(
                    "input <{input_name}> for 'setModel' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(model),
                            type_name_1 = CustomModel.CustomSqlModel,
                            type_name_2 = None
                        )
                )
        self._model = model

    def updatePanel(self, *args):
        if self.evaluator() and self.model():
            for i in range(self.evaluator().mainWidget().count()-1, -1, -1):
                evaluatorTab = self.evaluator().mainWidget().widget(i)
                evaluatorTab.clearTab()
                self.evaluator().mainWidget().removeTab(i)
            self.evaluator().createTabs(self.evaluator().dataFromModel())
            self.evaluator().plotData(self.evaluator().dataFromModel())

    def onTabBarClicked(self, index):
        if index <= 0:
            return
        progress = ProgressDialog.ProgressWindow(
                self,
                message = "update panel..."
            )
        self.updatePanel()
        progress.deleteLater()


