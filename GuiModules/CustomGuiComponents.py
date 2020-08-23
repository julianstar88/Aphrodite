# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string
import sys
import datetime
import re
import pathlib2
from UtilityModules.GraphicUtilityModules import CreateCanvas, CreateQPixmap
from MainModules.Database import database

from PyQt5 import QtWidgets, QtCore, QtGui

class CustomAddAlternativeDialog(QtWidgets.QDialog):

    ObjectType = "CustomAddAlternativeDialog"

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Create a new Trainingalternative")
        self.toCommit = {}

        # 1: Groups
        self.alternativeGroup = QtWidgets.QWidget(self)
        self.alternativeSubGroup1 = QtWidgets.QWidget(self)
        self.alternativeSubGroup2 = QtWidgets.QWidget(self)
        self.editorGroup = QtWidgets.QWidget(self)
        self.buttonGroup = QtWidgets.QWidget(self)

        # 2: Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.alternativeLayout = QtWidgets.QHBoxLayout(self.alternativeGroup)
        self.alternativeLayout.setContentsMargins(0,0,0,0)
        self.alternativeSubLayout1 = QtWidgets.QFormLayout(self.alternativeSubGroup1)
        self.alternativeSubLayout1.setContentsMargins(0,0,0,0)
        self.alternativeSubLayout2 = QtWidgets.QVBoxLayout(self.alternativeSubGroup2)
        self.alternativeSubLayout2.setContentsMargins(0,0,0,0)
        self.editorLayout = QtWidgets.QVBoxLayout(self.editorGroup)
        self.editorLayout.setContentsMargins(0,0,0,0)
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonGroup)
        self.buttonLayout.setContentsMargins(0,0,0,0)

        # 3: Members
        self.acceptButton = QtWidgets.QPushButton("OK", self.buttonGroup)
        self.acceptButton.setDefault(True)
        self.acceptButton.setEnabled(False)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self.buttonGroup)
        self.exerciseIdEdit = QtWidgets.QLineEdit(self.alternativeGroup)
        self.exerciseIdEdit.setPlaceholderText("New Exercise ID...")
        self.exerciseIdEdit.setValidator(QtGui.QIntValidator(self.exerciseIdEdit))
        self.shortNameEdit = QtWidgets.QLineEdit(self.alternativeGroup)
        self.shortNameEdit.setPlaceholderText("New Short Name...")
        self.editor = CustomRoutineEditor(parent = self.editorGroup)
        self.editor.verticalHeader().hide()
        items = [QtGui.QStandardItem(None) for item in range(self.editor.model().columnCount())]
        self.editor.model().appendRow(items)
        index = self.editor.model().index(0, 10)
        comboMode = CustomComboBox(self.editor)
        comboMode.insertItems(0, [], mode = "modes")
        self.editor.setIndexWidget(index, comboMode)

        index = self.editor.model().index(0, 0)
        comboAlt = CustomComboBox(self.editor)
        comboAlt.insertItems(0, [], mode = "gym")
        self.editor.setIndexWidget(index, comboAlt)

        comboMode.currentTextChanged.connect(
                comboAlt.onTextChanged
            )



        # 4: Layout Settings
        self.mainLayout.addWidget(self.alternativeGroup)
        self.mainLayout.addWidget(self.editorGroup)
        self.mainLayout.addWidget(self.buttonGroup)

        self.alternativeLayout.addWidget(self.alternativeSubGroup1)
        self.alternativeLayout.addStretch()
        self.alternativeLayout.addStretch()
        self.alternativeLayout.addWidget(self.alternativeSubGroup2)

        self.alternativeSubLayout1.addRow("Exercise ID:", self.exerciseIdEdit)
        self.alternativeSubLayout1.addRow("Short Name:", self.shortNameEdit)

        self.editorLayout.addWidget(self.editor)

        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # 5: Connectios
        self.exerciseIdEdit.textEdited.connect(self.onExerciseIdChanged)
        self.shortNameEdit.textEdited.connect(self.onShortNameChanged)

        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)

        # 6: Help
        self.__setHelp()

        # 7: Window Geometry
        width = self.editor.horizontalHeader().length()
        self.setGeometry(200,100,width,300)

        # 8: Show Dialog
        self.exec()

    def __setHelp(self):
        # Exercise ID
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Exercise ID for the new Trainingalternative.</b>
        </p>

        <p>
        The Exercise ID is a unique Number specifying to which Exercise this
        Alternative belongs. The new Alternative (as well as a generated Superscript)
        will be added to the Trainingroutine. The Value entered must be a <i>integer</i>!
        </p>
        """

        toolTip = """
        <p style='text-align:left'>
        Enter the Exercise ID for the new Trainingalternative
        </p>
        """
        self.exerciseIdEdit.setWhatsThis(whatsThis)
        self.exerciseIdEdit.setToolTip(toolTip)

        # Short Name
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Short Name for the new Trainingalternative.</b>
        </p>

        <p>
        The purpose of the Short Name is to be displayed, whenever a summary of
        all Alternative is neccessary (e.g. if if a note should be deleted via the
        <i>Delete Trainingalternative...</i> Dialog). The entered Value can be a
        <i>character vector</i> or a <i>string scalar</i>.
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Enter the Short Name for the new Trainingalternative
        </p>
        """
        self.shortNameEdit.setWhatsThis(whatsThis)
        self.shortNameEdit.setToolTip(toolTip)

    def onAcceptButtonClicked(self):
        model = self.editor.model()
        data = [
                eval(self.exerciseIdEdit.text()),
                self.shortNameEdit.text()
            ]
        for i in range(model.columnCount()):
            index = model.index(0,i)
            item = model.item(0,i)
            if i == 0:
                data.append(self.editor.indexWidget(index).currentText())
            elif i == model.columnCount()-1:
                data.append(self.editor.indexWidget(index).currentText())
            else:
                text = item.data(role = QtCore.Qt.DisplayRole)
                if not text:
                    text = None
                data.append(text)
        self.toCommit["alternative_values"] = data


    def onExerciseIdChanged(self, value):
        if self.exerciseIdEdit.text() == "" or self.shortNameEdit.text() == "":
            self.acceptButton.setEnabled(False)
        else:
            self.acceptButton.setEnabled(True)

    def onShortNameChanged(self, value):
        if self.exerciseIdEdit.text() == "" or self.shortNameEdit.text() == "":
            self.acceptButton.setEnabled(False)
        else:
            self.acceptButton.setEnabled(True)

class CustomDialogBase(QtWidgets.QDialog):

    ObjectType = "CustomBaseDialog"

    def __init__(self, *args, customIconPath = None):
        super().__init__(*args)
        self._customIconPath = None

        if customIconPath:
            self.setCustomIconPath(customIconPath)
        else:
            self.setCustomIconPath("files/icons/app_icons/")

        self.setCustomIcon()


    def customIconPath(self):
        return self._customIconPath

    def setCustomIcon(self, iconPath = None):
        if iconPath:
            self.setCustomIconPath(iconPath)
            
        icons = [
                ("Aphrodite8x8.png", (8, 8)),
                ("Aphrodite20x20.png", (20, 20)),
                ("Aphrodite16x16.png", (16, 16)),
                ("Aphordite24x24.png", (24, 24)),
                ("Aphrodite32x32.png", (32, 32)),
                ("Aphrodite40x40.png", (40, 40)),
                ("Aphrodite48x48.png", (48, 48)),
                ("Aphrodite56x56.png", (56, 56)),
                ("Aphrodite62x62.png", (62, 62)),
                ("Aphrodite64x64.png", (64, 64)),
                ("Aphrodite70x70.png", (70, 70)),
                ("Aphrodite78x78.png", (78, 78)),
                ("Aphrodite86x86.png", (86, 86)),
                ("Aphrodite94x94.png", (94, 94)),
                ("Aphrodite96x96.png", (96, 96)),
                ("Aphrodite128x128.png", (128, 128)),
                ("Aphrodite256x256.png", (256, 256))
            ]
        qIcon = QtGui.QIcon(str(self.customIconPath() / pathlib2.Path("Aphrodite96x96.png")))
        for icon in icons:
            file = self.customIconPath() / pathlib2.Path(icon[0])
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Normal, QtGui.QIcon.On)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Disabled, QtGui.QIcon.On)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Active, QtGui.QIcon.On)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Selected, QtGui.QIcon.On)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Active, QtGui.QIcon.Off)
            qIcon.addFile(str(file), QtCore.QSize(icon[1][0], icon[1][1]), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        self.setWindowIcon(qIcon)

    def setCustomIconPath(self, path):
        if (not isinstance(path, str)) and (not isinstance(path, pathlib2.Path)):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = str,
                            type_name_2 = pathlib2.Path
                        )
                )
        path = pathlib2.Path(path)
        if not path.is_dir():
            raise ValueError(
                    "<{path_name}> does not point to an existing directory".format(
                            path_name = path
                        )
                )
        self._customIconPath = path

class CustomBoxLayout(QtWidgets.QBoxLayout):

    ObjectType = "CustomBoxLayout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeConstraint(QtWidgets.QBoxLayout.SetMinAndMaxSize)

class CustomCalendarWidget(QtWidgets.QCalendarWidget):

    resetSelection = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)

    def contextMenuEvent(self, event):
        self.resetSelection.emit()
        super().contextMenuEvent(event)

class CustomComboBox(QtWidgets.QComboBox):

    ObjectType = "CustomComboBox"

    def __init__(self, *args):
        super().__init__(*args)
        self.text = {
                "exercises_gym":[
                        "Bankdrücken KH",
                        "Bankdrücken LH",
                        "Bankdrücken M",
                        "Bauch variationen",
                        "Bizeps KH",
                        "Bizeps Seilzug",
                        "Bizeps SZ",
                        "Bizeps LH",
                        "Bizeps Scott Curles",
                        "Butterfly KH",
                        "Butterfly Maschine",
                        "Klimmzüge F",
                        "Klimmzüge M",
                        "Kniebeugen F",
                        "Kniebeugen M",
                        "Rudern sitzend",
                        "Rudern vorgebeugt",
                        "Seitenheben KH",
                        "Seitenheben M",
                        "Trizeps Dips F",
                        "Trizeps Dips M",
                        "Trizeps Seilzug"
                    ],
                "exercises_running":[
                        "2K Interval",
                        "4K Interval",
                        "8K Interval",
                        "10K Interval",
                        "15K Interval",
                        "20K Interval",
                        "Halfmarathon",
                        "Long Distance"
                    ],
                "modes":[
                        "gym",
                        "interval",
                        "distance"
                    ]
            }

    def insertItems(self, index, itemList, mode = None):
        if mode:
            if mode == "gym":
                itemList = self.text["exercises_gym"]
            elif mode == "interval":
                itemList = self.text["exercises_running"]
            elif mode == "distance":
                itemList = self.text["exercises_running"]
            elif mode == "modes":
                itemList = self.text["modes"]

        super().insertItems(index, itemList)

    def onTextChanged(self, text):
        self.clear()
        self.insertItems(0, [], mode = text)

class CustomCreateNewRoutineDialog(CustomDialogBase):

    def __init__(self, configParser, *args, parent = None, windowTitle = "Create new Trainingroutine..."):
        super().__init__(parent, *args)
        self._toCommit = dict()
        self._configParser = None
        self.setConfigParser(configParser)

        self.setWindowTitle(windowTitle)

        self.configParser().readConfigFile()

        # Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.informationLayout = QtWidgets.QFormLayout()
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Members
        self.trainingRoutineEdit = QtWidgets.QLineEdit(self)
        self.trainingRoutineEdit.setPlaceholderText("Enter Trainingroutines Name...")

        self.nameEdit = QtWidgets.QLineEdit(self)
        self.nameEdit.setPlaceholderText("Enter Username...")

        self.trainingModeEdit = QtWidgets.QLineEdit(self)
        self.trainingModeEdit.setPlaceholderText("Enter Trainingmode...")

        self.startDateEdit = QtWidgets.QDateEdit(self)
        self.startDateEdit.setDate(QtCore.QDate().currentDate())
        self.startDateEdit.setCalendarPopup(True)

        self.endDateView = QtWidgets.QDateEdit(self)
        self.endDateView.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setEndDate()
        self.endDateView.setReadOnly(True)

        self.pathEdit = QtWidgets.QLineEdit(self)
        self.pathEdit.setPlaceholderText("Enter Save Path...")

        self.dirButton = QtWidgets.QPushButton("Choose Directory...", self)
        self.acceptButton = QtWidgets.QPushButton("OK")
        self.acceptButton.setDefault(True)
        self.acceptButton.setEnabled(False)
        self.rejectButton = QtWidgets.QPushButton("Cancel")

        self.dirDialog = QtWidgets.QFileDialog(self) 
        self.dirDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)


        # Layout Settings
        self.mainLayout.addLayout(self.informationLayout)
        self.mainLayout.addLayout(self.buttonLayout)

        self.informationLayout.addRow("Trainingroutine:", self.trainingRoutineEdit)
        self.informationLayout.addRow("Name:", self.nameEdit)
        self.informationLayout.addRow("Trainingmode:", self.trainingModeEdit)
        self.informationLayout.addRow("Start:", self.startDateEdit)
        self.informationLayout.addRow("End:", self.endDateView)
        self.informationLayout.addRow("Save Path:", self.pathEdit)

        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.dirButton)
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # Connections
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAccepted)
        self.rejectButton.clicked.connect(self.reject)
        self.startDateEdit.dateChanged.connect(self.setEndDate)
        self.startDateEdit.dateChanged.connect(self.setTrainingRoutine)
        self.pathEdit.textChanged.connect(self.onPathChanged)
        self.dirButton.clicked.connect(self.onChooseDirectory)

        # Populate Dialog
        self.populateDialogMembers()

        # Show Dialog
        self.exec()

    def calculateTrainingPeriode(self, startDateStr):
        if isinstance(startDateStr, QtCore.QDate):
            startDate = startDateStr
            endDate = startDate.addDays(42)
        elif isinstance(startDateStr, str):
            match = re.search("(?P<day>\d+).(?P<month>\d+).(?P<year>\d+)", startDateStr)
            startDate = QtCore.QDate(
                    int(match.group("year")),
                    int(match.group("month")),
                    int(match.group("day"))
                )
            endDate = startDate.addDays(42)
        else:
            date = datetime.date.today()
            startDate = QtCore.QDate(date.year, date.month, date.day)
            endDate = startDate.addDays(42)
        return [startDate, endDate]

    def configParser(self):
        return self._configParser

    def defaultDirectory(self, *args):
        path = self.configParser().readAttributes()["new_routine_directory"]
        if path:
            pathObj = pathlib2.Path(path)
        else:
            pathObj = pathlib2.Path().cwd() / "training_routines"
        return pathObj

    def onAccepted(self):
        generalData = list()

        databaseName = self.trainingRoutineEdit.text()
        self.setToCommit("databaseName", databaseName)

        username = self.nameEdit.text()
        generalData.append(username)
        startDate = self.startDateEdit.date()
        strDate = startDate.toString("dd.MM.yyyy")
        generalData.append(strDate)
        trainingMode = self.trainingModeEdit.text()
        generalData.append(trainingMode)
        self.setToCommit("general_information", generalData)

        savePath = pathlib2.Path(self.pathEdit.text())
        self.setToCommit("new_routine_directory", str(savePath))

    def onChooseDirectory(self, *args):
        default = QtCore.QDir(str(self.defaultDirectory()))
        self.dirDialog.setDirectory(default)
        directory = self.dirDialog.getExistingDirectory(self.dirDialog, "Choose Directory")

        if not directory:
            return False

        self.pathEdit.setText(directory)

    def onPathChanged(self, *args):
        if self.pathEdit.text():
            self.acceptButton.setEnabled(True)
        else:
            self.acceptButton.setEnabled(False)

    def populateDialogMembers(self, *args):
        self.setTrainingRoutine()
        self.pathEdit.setText(str(self.defaultDirectory()))
        self.pathEdit.setCursorPosition(len(self.pathEdit.text()))

    def setConfigParser(self, configParser):
        self._configParser = configParser

    def setEndDate(self, *args):
        periode = self.calculateTrainingPeriode(self.startDateEdit.date())
        self.endDateView.setDate(periode[1])

    def setToCommit(self, key, value):
        self._toCommit[key] = value

    def setTrainingRoutine(self, *args):
        date = self.startDateEdit.date()
        dateStr = date.toString("yyMMdd")
        trainingRoutine = "Training-" + dateStr
        self.trainingRoutineEdit.setText(trainingRoutine)

    def toCommit(self):
        return self._toCommit

class CustomEditAlternativesDialog(CustomDialogBase):

    def __init__(self, database, *args, parent = None, windowTitle = "Edit Trainingalternatives..."):
        super().__init__(parent, *args)
        self._toCommit = None
        self._database = None
        self._movedRows = list()
        self.setDatabase(database)

        self.setWindowTitle(windowTitle)

        # Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Members
        self.editor = CustomRoutineEditor(
                parent = self,
                modelRows = 0,
                modelColumns = 14,
                rowsMovable = True,
            )
        labels = [
                "Exercise ID",
                "Label",
                "Short",
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
            ]
        self.editor.model().setHorizontalHeaderLabels(labels)
        self.editor.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.editor.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        self.editor.setTabKeyNavigation(False)


        self.acceptButton = QtWidgets.QPushButton("OK", self)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self)

        # Layout Setting
        self.mainLayout.addWidget(self.editor)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)
        self.mainLayout.addLayout(self.buttonLayout)

        # connections
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)
        self.editor.wheelTurned.connect(self.onWheelTurned)
        self.editor.rowHasBeenMoved.connect(self.onRowMoved)

        # Window Geometry
        width = self.editor.horizontalHeader().length()
        self.setGeometry(200,100,width,500)
        self.editor.resizeColumnToContent(3)

        # populate editor model
        self.populateEditorModel()

        # Show Dialog
        self.exec()

    def __displayException(self, exceptionType, value, traceBack):
        string = "Traceback: {traceback} \n Exception Type: {etype} \n Value: {value}".format(
                traceback = traceBack,
                etype = exceptionType,
                value = str(value)
            )
        print(string)

    def database(self):
        return self._database

    def movedRows(self):
        return self._movedRows

    def onAcceptButtonClicked(self, debugging = False):
        rows = self.editor.model().rowCount()
        cols = self.editor.model().columnCount()

        for n in range(rows):
            for m in range(cols):
                item = self.editor.model().item(n, m)
                index = self.editor.model().indexFromItem(item)
                if (m == 3 or m == 13):
                    combo = self.editor.indexWidget(index)
                    item.setData(combo.currentText(), QtCore.Qt.DisplayRole)

        for moved in self.movedRows():
            row = self.editor.model().takeRow(moved[0])
            self.editor.model().insertRow(moved[1], row)

        data = list()
        for n in range(rows):
            line = list()
            for m in range(cols):
                item = self.editor.model().item(n, m)
                val = item.data(QtCore.Qt.DisplayRole)
                if m == 0:
                    try:
                        line.append(eval(val))
                    except:
                        if debugging:
                            print("CustomEditAlternativesDialog: couldn´t evaluate <{input_name}> for 'exerciseID' in line '{line_num}'. input has to be {type_name}. set value to 'None'".format(
                                    input_name = str(val),
                                    line_num = str(n),
                                    type_name = int
                                ))
                            etype, value, traceBack = sys.exc_info()
                            self.__displayException(etype, value, traceBack)
                        line.append(None)
                else:
                    line.append(val)
            data.append(line)

        self.setToCommit(data)

    def onRowMoved(self, fromRow, toRow):
        movedRows = self.movedRows()
        movedRows.append([fromRow, toRow])
        self.setMovedRows(movedRows)

    def onWheelTurned(self, obj, event):
        angle = event.angleDelta().y()
        model = self.editor.model()
        if angle < 0:
            oldRowCount = model.rowCount()
            items = [QtGui.QStandardItem(None) for item in range(model.columnCount())]
            model.appendRow(items)
            newRowCount = model.rowCount()

            items[1].setText(str(newRowCount))
            items[2].setText("alternative {}".format(newRowCount))

            for i in range(oldRowCount, newRowCount+1, 1):
                index = model.index(i, 13)
                modeCombo = CustomComboBox(self.editor)
                modeCombo.insertItems(0, [], mode = "modes")
                self.editor.setIndexWidget(index, modeCombo)

                index = model.index(i, 3)
                exerciseCombo = CustomComboBox(self.editor)
                exerciseCombo.insertItems(0, [], mode = "gym")
                self.editor.setIndexWidget(index, exerciseCombo)

                modeCombo.currentTextChanged.connect(
                        exerciseCombo.onTextChanged
                    )

        if angle > 0:
            oldValue = model.rowCount()
            newValue = oldValue-1
            for i in range(oldValue, newValue-1, -1):
                model.removeRow(i)
                self.editor.rowCountChanged(oldValue, newValue)

    def populateEditorModel(self):
        if not self.database().isValid():
            return False

        data = self.database().data("training_alternatives")
        modelData = list()
        for row in data:
            line = [QtGui.QStandardItem(str(row[i])) for i in range(len(row))]

            if row[0] is None:
                line[0] = QtGui.QStandardItem(None)

            modelData.append(line)

        for row in modelData:
            self.editor.model().appendRow(row)

        for i in range(len(data)):
            exerciseCombo = CustomComboBox()
            exerciseCombo.insertItems(0, [], mode = "gym")
            text = data[i][3]
            index = exerciseCombo.findText(text)
            exerciseCombo.setCurrentIndex(index)

            modeCombo = CustomComboBox()
            modeCombo.insertItems(0, [], mode = "modes")
            text = data[i][-1]
            index = modeCombo.findText(text)
            modeCombo.setCurrentIndex(index)

            modelIndexCombo = self.editor.model().index(i, 3)
            modelIndexMode = self.editor.model().index(i, 13)
            self.editor.setIndexWidget(modelIndexCombo, exerciseCombo)
            self.editor.setIndexWidget(modelIndexMode, modeCombo)

        return True

    def setDatabase(self, database):
        self._database = database

    def setMovedRows(self, moved):
        self._movedRows = moved

    def setToCommit(self, data):
        self._toCommit = data

    def toCommit(self):
        return self._toCommit

class CustomEditNotesDialog(CustomDialogBase):

    lowercaseLetters = string.ascii_lowercase

    def __init__(self, database, *args, parent = None, windowTitle = "Edit Trainingnotes..."):
        super().__init__(parent, *args)
        self._toCommit = None
        self._database = None
        self._movedRows = list()
        self.setDatabase(database)

        self.setWindowTitle(windowTitle)

        # Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Members
        self.editor = CustomRoutineEditor(
                parent = self,
                modelRows = 0,
                modelColumns = 4,
                rowsMovable = True,
            )
        labels = [
                "Exercise ID",
                "Label",
                "Short",
                "Note"
            ]
        self.editor.model().setHorizontalHeaderLabels(labels)
        self.editor.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.editor.setTabKeyNavigation(False)

        self.acceptButton = QtWidgets.QPushButton("OK", self)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self)

        # Layout Setting
        self.mainLayout.addWidget(self.editor)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)
        self.mainLayout.addLayout(self.buttonLayout)

        # connections
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)
        self.editor.wheelTurned.connect(self.onWheelTurned)
        self.editor.activated.connect(self.onActivated)
        self.editor.rowHasBeenMoved.connect(self.onRowMoved)
        # self.editor.doubleClicked.connect(self.onActivated)

        # Window Geometry
        size = self.editor.horizontalHeader().sectionSize(0)
        self.editor.horizontalHeader().setMinimumSectionSize(size)
        for i in range(self.editor.horizontalHeader().count()):
            self.editor.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
        self.editor.horizontalHeader().setStretchLastSection(True)
        self.setGeometry(200,100,800,500)

        # populate editor model
        self.populateEditorModel()

        # Show Dialog
        self.exec()

    def __displayException(self, exceptionType, value, traceBack):
        string = "Traceback: {traceback} \n Exception Type: {etype} \n Value: {value}".format(
                traceback = traceBack,
                etype = exceptionType,
                value = str(value)
            )
        print(string)

    def keyPressEvent(self, event):

        # ignore Return or Enter Key to prevent unwanted dialog closing
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            return event.ignore()

        return super().keyPressEvent(event)

    def database(self):
        return self._database

    def movedRows(self):
        return self._movedRows

    def onAcceptButtonClicked(self, debugging = False):
        rows = self.editor.model().rowCount()
        cols = self.editor.model().columnCount()

        for moved in self.movedRows():
            row = self.editor.model().takeRow(moved[0])
            self.editor.model().insertRow(moved[1], row)

        data = list()
        for n in range(rows):
            line = list()
            for m in range(cols):
                item = self.editor.model().item(n, m)
                val = item.data(QtCore.Qt.DisplayRole)
                if m == 0:
                    try:
                        line.append(eval(val))
                    except:
                        if debugging:
                            print("CustomEditNotesDialog: couldn´t evaluate <{input_name}> for 'exerciseID' in line '{line_num}'. input has to be {type_name}. set value to 'None'".format(
                                    input_name = str(val),
                                    line_num = str(n),
                                    type_name = int
                                ))
                            etype, value, traceBack = sys.exc_info()
                            self.__displayException(etype, value, traceBack)
                        line.append(None)
                else:
                    line.append(val)
            data.append(line)

        self.setToCommit(data)

    def onActivated(self, modelIndex):
        text = modelIndex.data(QtCore.Qt.DisplayRole)
        headerLabels = list()
        for i in range(self.editor.horizontalHeader().count()):
            headerLabels.append(self.editor.model().horizontalHeaderItem(i).text())

        title = "Edit {}...".format(headerLabels[modelIndex.column()])
        dialog = CustomEnterTextDialog(
                text,
                parent = self.editor,
                dialogTitle = title
            )
        item = modelIndex.model().itemFromIndex(modelIndex)

        if dialog.result():
            item.setText(dialog.toCommit())
        else:
            item.setText(text)

    def onRowMoved(self, fromRow, toRow):
        movedRows = self.movedRows()
        movedRows.append([fromRow, toRow])
        self.setMovedRows(movedRows)

    def onWheelTurned(self, obj, event):
        angle = event.angleDelta().y()
        model = self.editor.model()
        if angle < 0:
            oldRowCount = model.rowCount()
            items = [QtGui.QStandardItem(None) for item in range(model.columnCount())]
            model.appendRow(items)
            newRowCount = model.rowCount()

            items[0].setText("")
            items[1].setText(type(self).lowercaseLetters[oldRowCount])
            items[2].setText("note {}".format(newRowCount))
            items[3].setEditable(False)

        if angle > 0:
            oldValue = model.rowCount()
            newValue = oldValue-1
            for i in range(oldValue, newValue-1, -1):
                model.removeRow(i)
                self.editor.rowCountChanged(oldValue, newValue)

    def populateEditorModel(self):
        if not self.database().isValid():
            return False

        data = self.database().data("training_notes")
        modelData = list()
        for row in data:
            line = [QtGui.QStandardItem(str(row[i])) for i in range(len(row))]

            if row[0] is None:
                line[0] = QtGui.QStandardItem(None)

            modelData.append(line)

        for row in modelData:
            self.editor.model().appendRow(row)

        for n in range(self.editor.model().rowCount()):
            for m in range(self.editor.model().columnCount()):
                if m == 3:
                    item = self.editor.model().item(n, m)
                    item.setEditable(False)

        return True

    def setDatabase(self, database):
        self._database = database

    def setMovedRows(self, moved):
        self._movedRows = moved

    def setToCommit(self, data):
        self._toCommit = data

    def toCommit(self):
        return self._toCommit

class CustomEditRoutineDialog(CustomDialogBase):

    def __init__(self, database, *args, parent = None, windowTitle = "Edit Trainingroutine..."):
        super().__init__(parent, *args)
        self._database = None
        self._toCommit = dict()
        self._movedRows = list()

        self.setWindowTitle(windowTitle)

        self.setDatabase(database)

        # Groups
        self.GeneralInformationGroup = QtWidgets.QGroupBox("General Information", self)

        # Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.GeneralInformationLayout = QtWidgets.QGridLayout(self.GeneralInformationGroup)
        self.userInformationLayout = QtWidgets.QFormLayout()
        self.dialogButtonLayout = QtWidgets.QHBoxLayout()

        # Members
        self.editAlternativesButton = QtWidgets.QPushButton("Edit Alternatives...", self)
        self.editNotesButton = QtWidgets.QPushButton("Edit Notes...", self)
        self.acceptButton = QtWidgets.QPushButton("OK", self)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self)
        self.usernameEdit = QtWidgets.QLineEdit(self)
        self.usernameEdit.setPlaceholderText("Enter Name...")
        self.trainingmodeEdit = QtWidgets.QLineEdit(self)
        self.trainingmodeEdit.setPlaceholderText("Enter Trainingmode...")

        self.editor = CustomRoutineEditor(
                parent = self,
                modelRows = 0,
                modelColumns = 10,
                rowsMovable = True,
            )
        self.editor.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.editor.setTabKeyNavigation(False)

        self.trainingPeriodeSelector = CustomCalendarWidget(self)
        self.trainingPeriodeSelector.setSelectionMode(QtWidgets.QCalendarWidget.NoSelection)
        self.trainingPeriodeSelector.resetSelection.connect(self.onSelectionReset)
        self.trainingPeriodeSelector.selectionChanged.connect(self.onSelectedDateChanged)

        self.startDateSelector = QtWidgets.QDateEdit(self)
        self.startDateSelector.dateChanged.connect(self.onStartDateChanged)
        self.endDateView = QtWidgets.QDateEdit(self)
        self.endDateView.setReadOnly(True)
        self.endDateView.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        # Layout Settings
        self.mainLayout.addWidget(self.GeneralInformationGroup)
        self.mainLayout.addWidget(self.editor)
        self.mainLayout.addLayout(self.dialogButtonLayout)

        self.GeneralInformationLayout.addLayout(self.userInformationLayout, 0, 0, 1, 1)
        self.GeneralInformationLayout.addWidget(self.trainingPeriodeSelector, 0, 1, 1, 1)
        self.GeneralInformationLayout.setColumnStretch(0, 1)
        self.GeneralInformationLayout.setColumnStretch(1, 3)
        self.userInformationLayout.addRow("Name:", self.usernameEdit)
        self.userInformationLayout.addRow("Trainingmode:", self.trainingmodeEdit)
        self.userInformationLayout.addRow("Start:", self.startDateSelector)
        self.userInformationLayout.addRow("End:", self.endDateView)

        self.dialogButtonLayout.addStretch()
        self.dialogButtonLayout.addWidget(self.editAlternativesButton)
        self.dialogButtonLayout.addWidget(self.editNotesButton)
        self.dialogButtonLayout.addWidget(self.acceptButton)
        self.dialogButtonLayout.addWidget(self.rejectButton)

        # dialog settings
        self.populateDialogMembers()

        # Connections
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)
        self.editor.wheelTurned.connect(self.onWheelTurned)
        self.editor.rowHasBeenMoved.connect(self.onRowMoved)
        self.editAlternativesButton.clicked.connect(self.onEditAlternatives)
        self.editNotesButton.clicked.connect(self.onEditNotes)

        # Window Geometry
        width = self.editor.horizontalHeader().length()
        self.setGeometry(200,100,width,500)
        self.editor.resizeColumnToContent(0)

        # Show Dialog
        self.exec()

    def __displayException(self, exceptionType, value, traceBack):
        string = "Traceback: {traceback} \n Exception Type: {etype} \n Value: {value}".format(
                traceback = traceBack,
                etype = exceptionType,
                value = str(value)
            )
        print(string)

    def calculateTrainingPeriode(self, startDateStr):
        if isinstance(startDateStr, QtCore.QDate):
            startDate = startDateStr
            endDate = startDate.addDays(42)
        elif isinstance(startDateStr, str):
            match = re.search("(?P<day>\d+).(?P<month>\d+).(?P<year>\d+)", startDateStr)
            startDate = QtCore.QDate(
                    int(match.group("year")),
                    int(match.group("month")),
                    int(match.group("day"))
                )
            endDate = startDate.addDays(42)
        else:
            date = datetime.date.today()
            startDate = QtCore.QDate(date.year, date.month, date.day)
            endDate = startDate.addDays(42)
        return [startDate, endDate]


    def database(self):
        return self._database

    def movedRows(self):
        return self._movedRows

    def onAcceptButtonClicked(self):
        rows = self.editor.model().rowCount()
        cols = self.editor.model().columnCount()

        for n in range(rows):
            for m in range(cols):
                item = self.editor.model().item(n, m)
                index = self.editor.model().indexFromItem(item)
                if (m == 0 or m == 10):
                    combo = self.editor.indexWidget(index)
                    item.setData(combo.currentText(), QtCore.Qt.DisplayRole)

        for moved in self.movedRows():
            row = self.editor.model().takeRow(moved[0])
            self.editor.model().insertRow(moved[1], row)

        data = list()
        for n in range(rows):
            line = list()
            for m in range(cols):
                item = self.editor.model().item(n, m)
                val = item.data(QtCore.Qt.DisplayRole)
                line.append(val)
            data.append(line)

        self.setToCommit("training_routine", data)

        data = list()
        name = self.usernameEdit.text()
        date = self.startDateSelector.date()
        dateObj = datetime.date(date.year(), date.month(), date.day())
        startDate = dateObj.strftime("%d.%m.%Y")
        mode = self.trainingmodeEdit.text()

        # name, startDate and mode have to be in a nested list, to use
        # Database.database.addManyEntries uniformly to the other tables
        self.setToCommit("general_information", [[name, startDate, mode]])

    def onEditAlternatives(self):
        dialog = CustomEditAlternativesDialog(
                self.database(),
                parent = self
            )
        if dialog.result():
            self.database().deleteAllEntries("training_alternatives")
            self.database().addManyEntries("training_alternatives", dialog.toCommit())

    def onEditNotes(self):
        dialog = CustomEditNotesDialog(
                self.database(),
                parent = None
            )
        if dialog.result():
            self.database().deleteAllEntries("training_notes")
            self.database().addManyEntries("training_notes", dialog.toCommit())

    def onRowMoved(self, fromRow, toRow):
        movedRows = self.movedRows()
        movedRows.append([fromRow, toRow])
        self.setMovedRows(movedRows)

    def onSelectedDateChanged(self):
        date = self.trainingPeriodeSelector.selectedDate()
        self.onStartDateChanged(date)

    def onSelectionReset(self):
        currentYear = QtCore.QDate.currentDate().year()
        minDate = QtCore.QDate(currentYear, 1, 1)
        maxDate = QtCore.QDate(currentYear + 1, 12, 31)
        self.trainingPeriodeSelector.setDateRange(minDate, maxDate)
        self.trainingPeriodeSelector.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)

    def onStartDateChanged(self, date):
        trainingPeriode = self.calculateTrainingPeriode(date)
        self.startDateSelector.setDate(trainingPeriode[0])
        self.endDateView.setDate(trainingPeriode[1])
        self.trainingPeriodeSelector.setDateRange(trainingPeriode[0], trainingPeriode[1])
        self.trainingPeriodeSelector.setSelectionMode(QtWidgets.QCalendarWidget.NoSelection)

    def onWheelTurned(self, obj, event):
        angle = event.angleDelta().y()
        model = self.editor.model()
        if angle < 0:
            oldRowCount = model.rowCount()
            items = [QtGui.QStandardItem(None) for item in range(model.columnCount())]
            model.appendRow(items)
            newRowCount = model.rowCount()

            # items[0].setText("None")
            # items[1].setText(str(newRowCount))
            # items[2].setText("alternative {}".format(newRowCount))

            for i in range(oldRowCount, newRowCount+1, 1):
                index = model.index(i, 10)
                modeCombo = CustomComboBox(self.editor)
                modeCombo.insertItems(0, [], mode = "modes")
                self.editor.setIndexWidget(index, modeCombo)

                index = model.index(i, 0)
                exerciseCombo = CustomComboBox(self.editor)
                exerciseCombo.insertItems(0, [], mode = "gym")
                self.editor.setIndexWidget(index, exerciseCombo)

                modeCombo.currentTextChanged.connect(
                        exerciseCombo.onTextChanged
                    )

        if angle > 0:
            oldValue = model.rowCount()
            newValue = oldValue-1
            for i in range(oldValue, newValue-1, -1):
                model.removeRow(i)
                self.editor.rowCountChanged(oldValue, newValue)

    def populateDialogMembers(self):
        if not self.database().isValid():
            return False

        routineData = self.database().data("training_routine")
        generalData = self.database().data("general_information")

        labels = [
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
            ]
        self.editor.model().setHorizontalHeaderLabels(labels)
        for row in routineData:
            line = [QtGui.QStandardItem(row[i]) for i in range(len(row))]
            self.editor.model().appendRow(line)

        for i in range(len(routineData)):
            exerciseCombo = CustomComboBox()
            exerciseCombo.insertItems(0, [], mode = "gym")
            text = routineData[i][0]
            index = exerciseCombo.findText(text)
            exerciseCombo.setCurrentIndex(index)

            modeCombo = CustomComboBox()
            modeCombo.insertItems(0, [], mode = "modes")
            text = routineData[i][-1]
            index = modeCombo.findText(text)
            modeCombo.setCurrentIndex(index)

            modelIndexCombo = self.editor.model().index(i, 0)
            modelIndexMode = self.editor.model().index(i, 10)
            self.editor.setIndexWidget(modelIndexCombo, exerciseCombo)
            self.editor.setIndexWidget(modelIndexMode, modeCombo)

        try:
            self.usernameEdit.setText(generalData[0][0])
        except IndexError:
            pass

        try:
            self.trainingmodeEdit.setText(generalData[0][2])
        except IndexError:
            pass

        try:
            startDateStr = generalData[0][1]
        except IndexError:
            startDateStr = None

        trainingPeriode = self.calculateTrainingPeriode(startDateStr)
        self.startDateSelector.setDate(trainingPeriode[0])
        self.endDateView.setDate(trainingPeriode[1])
        self.trainingPeriodeSelector.setDateRange(trainingPeriode[0], trainingPeriode[1])
        return True

    def setDatabase(self, database):
        self._database = database

    def setMovedRows(self, moved):
        self._movedRows = moved

    def setToCommit(self, tableName, data):
        self._toCommit[tableName] = data

    def toCommit(self):
        return self._toCommit

class CustomEnterTextDialog(CustomDialogBase):

    def __init__(self, text, *args, parent = None, dialogTitle = "Edit..."):
        super().__init__(parent, *args)
        self.setWindowTitle(dialogTitle)
        self.setGeometry(100,200, 500, 300)
        self._editorText = None
        self._toCommit = None

        self.setEditorText(text)

        # layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # members
        self.editor = QtWidgets.QTextEdit(self)
        self.editor.insertHtml(self.editorText())
        self.editor.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.editor.setTabChangesFocus(True)
        self.editor.selectAll()

        self.acceptButton = QtWidgets.QPushButton("OK", self)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self)

        # layout settings
        self.mainLayout.addWidget(self.editor)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # connections
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)

        # show dialog
        self.exec()

    def editorText(self):
        return self._editorText

    def onAcceptButtonClicked(self):
        self.setToCommit(self.editor.toPlainText())

    def setEditorText(self, text):
        self._editorText = text

    def setToCommit(self, data):
        self._toCommit = data

    def toCommit(self):
        return self._toCommit

class CustomEventFilter(QtCore.QObject):

    def __init__(self, *args):
        super().__init__(*args)


    def eventFilter(self, obj, event):
        print(event.type())
        return False
    
class CustomIcon(QtGui.QIcon):
    
    def __init__(self, *args, appIcons = None, iconPath = None):
        super().__init__(*args)
        self._iconPath = pathlib2.Path("files/icons/app_icons")
        self._appIcons = [
                (pathlib2.Path("Aphrodite8x8.png"), (8, 8)),
                (pathlib2.Path("Aphrodite20x20.png"), (20, 20)),
                (pathlib2.Path("Aphrodite16x16.png"), (16, 16)),
                (pathlib2.Path("Aphordite24x24.png"), (24, 24)),
                (pathlib2.Path("Aphrodite32x32.png"), (32, 32)),
                (pathlib2.Path("Aphrodite40x40.png"), (40, 40)),
                (pathlib2.Path("Aphrodite48x48.png"), (48, 48)),
                (pathlib2.Path("Aphrodite56x56.png"), (56, 56)),
                (pathlib2.Path("Aphrodite62x62.png"), (62, 62)),
                (pathlib2.Path("Aphrodite64x64.png"), (64, 64)),
                (pathlib2.Path("Aphrodite70x70.png"), (70, 70)),
                (pathlib2.Path("Aphrodite78x78.png"), (78, 78)),
                (pathlib2.Path("Aphrodite86x86.png"), (86, 86)),
                (pathlib2.Path("Aphrodite94x94.png"), (94, 94)),
                (pathlib2.Path("Aphrodite96x96.png"), (96, 96)),
                (pathlib2.Path("Aphrodite128x128.png"), (128, 128)),
                (pathlib2.Path("Aphrodite256x256.png"), (256, 256))
            ]
        
        if appIcons:
            self.setAppIcons(appIcons)
            
        if iconPath:
            self.setIconPath(iconPath)
        
        for icon in self.appIcons():
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Normal, 
                QtGui.QIcon.On
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Disabled, 
                QtGui.QIcon.On
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Active, 
                QtGui.QIcon.On
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Selected, 
                QtGui.QIcon.On
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Normal, 
                QtGui.QIcon.Off
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Disabled, 
                QtGui.QIcon.Off
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Active, 
                QtGui.QIcon.Off
                )
            self.addFile(
                str(self.iconPath / icon[0]), 
                QtCore.QSize(icon[1][0], icon[1][1]), 
                QtGui.QIcon.Selected, 
                QtGui.QIcon.Off
                )
            
    def appIcons(self):
        return self._appIcons
    
    def iconPath(self):
        return self._iconPath
    
    def setAppIcons(self, icons):
        self._appIcons = icons
    
    def setIconPath(self, path):
        path = pathlib2.Path(path)
        self.iconPath = path

class CustomLabel(QtWidgets.QLabel):

    ObjectType = "CustomLabel"

    def __init__(self, QPixmap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = None
        self.setPixmap(QPixmap)
        self.setAutoFillBackground(False)

class CustomMessageBox(QtWidgets.QMessageBox):

    def __init__(
                self,
                message,
                icon = QtWidgets.QMessageBox.Warning,
                buttons = QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok,
                windowTitle = None,
                customIconPath = None
            ):
        super().__init__()
        self._customIconPath = None

        self.setText(message)
        self.setStandardButtons(buttons)
        self.setDefaultButton(QtWidgets.QMessageBox.Save)
        self.setIcon(icon)
        if windowTitle:
            self.setWindowTitle(windowTitle)
        else:
            if icon == QtWidgets.QMessageBox.Warning:
                self.setWindowTitle("Warning")
            elif icon == QtWidgets.QMessageBox.Critical:
                self.setWindowTitle("Error")
            else:
                self.setWindowTitle("Message")
        if customIconPath:
            self.setCustomIconPath(customIconPath)
        else:
            self.setCustomIconPath("files/icons/app_icons")

        self.setCustomIcon()

    def customIconPath(self):
        return self._customIconPath

    def message(self):
        return self._message

    def setCustomIcon(self, iconPath = None):
        if iconPath:
            self.setIconPath(iconPath)

        if self.customIconPath():
            # self.setWindowIcon(QtGui.QIcon(str(self.customIconPath())))
            self.setWindowIcon(CustomIcon(iconPath = str(self.customIconPath())))

    def setCustomIconPath(self, path):
        if (not isinstance(path, str)) and (not isinstance(path, pathlib2.Path)):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = str,
                            type_name_2 = pathlib2.Path()
                        )
                )
        path = pathlib2.Path(path)
        if not path.is_dir():
            raise ValueError(
                    "<{path_name}> does not point to an existing directory".format(
                            path_name = path
                        )
                )
        self._customIconPath = path

    def setMessage(self, message):
        self._message = message

class CustomModelItem(QtGui.QStandardItem):

    ObjectType = "CustomModelItem"

    trainingAlternatives = list()
    trainingNotes = list()
    lowercaseLetters = string.ascii_lowercase

    def __init__(self, displayData, *args):
        super().__init__(displayData, *args)
        self._userData = None

        self.setUserData(displayData)

    def addTrainingAlternative(self, exerciseID, alternativeExercise, warmUp, repetition,
                               w1, w2, w3, w4, w5, w6, mode,
                               label = None, short = None):
        # if not alternativeID:
        #     alternativeID = len(type(self).trainingAlternatives) + 1

        if not label:
            label = "{num}".format(num = str(len(type(self).trainingAlternatives) + 1))

        if not short:
            short = "alternative {num}".format(num = str(len(type(self).trainingAlternatives) + 1))

        data = [
                exerciseID,
                label,
                short,
                alternativeExercise,
                warmUp,
                repetition,
                w1,
                w2,
                w3,
                w4,
                w5,
                w6,
                mode
                ]
        type(self).trainingAlternatives.append(data)

    def addTrainingNote(self, exerciseID, short, note, label = None,):

        if not label:
            label = type(self).lowercaseLetters[len(type(self).trainingNotes)]

        data = [
                exerciseID,
                label,
                short,
                note,
            ]
        type(self).trainingNotes.append(data)

    def commitAlternativesToDatabase(self, database, table):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()

            # 1: delete the old talbe as it is no longer important
            sqlCommand = "DROP TABLE IF EXISTS {name}".format(name = table)
            c.execute(sqlCommand)

            # 2: create a new table
            values = """
                exerciseID INT,
                label TEXT,
                short TEXT,
                alternativ TEXT,
                Sets TEXT,
                Repetitions TEXT,
                Warm_Up TEXT,
                Week_1 TEXT,
                Week_2 TEXT,
                Week_3 TEXT,
                Week_4 TEXT,
                Week_5 TEXT,
                Week_6 TEXT
            """
            sqlCommand = "CREATE TABLE {name}({values})".format(
                name = table, values = values)
            c.execute(sqlCommand)

            # 3: insert the actual table into the new table
            values = "?, " * len(type(self).trainingAlternatives[0])
            values = values[:-2]
            sqlCommand = "INSERT INTO {name} VALUES({values})".format(
                    name = table,
                    values = values,
                )
            c.executemany(sqlCommand, type(self).trainingAlternatives)

        con.close()

    def commitNotesToDatabase(self, database, table):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()

            # 1: delete the old table because it´s not needed anymore
            sqlCommand = "DROP TABLE IF EXISTS {name}".format(name = table)
            c.execute(sqlCommand)

            # 2: create a new table
            values = """
                        exerciseID INT,
                        label TEXT,
                        short TEXT,
                        note TEXT
                    """
            sqlCommand = "CREATE TABLE {name}({values})".format(
                name = table, values = values)
            c.execute(sqlCommand)

            # 3: insert the actual values into the new table
            values = "?, " * len(type(self).trainingNotes[0])
            values = values[:-2]
            sqlCommand = "INSERT INTO {name} VALUES({values})".format(
                    name = table,
                    values = values,
                )
            c.executemany(sqlCommand, type(self).trainingNotes)

        con.close()

    def deleteTrainingAlternativ(self, index):
            try:
                del type(self).trainingAlternatives[index]
            except IndexError:
                return

    def deleteTrainingNote(self, index):
        try:
            del type(self).trainingNotes[index]
        except IndexError:
            return

    @staticmethod
    def fetchAlternativesFromDatabase(database):
        try:
            data = database.data("training_alternatives")
        except:
            con = sqlite3.connect(database)
            with con:
                c = con.cursor()
                sqlCommand = "SELECT * FROM training_alternatives"
                try:
                    c.execute(sqlCommand)
                except sqlite3.OperationalError:
                    return False
                data = c.fetchall()
            con.close()
            data = [list(item) for item in data]

        CustomModelItem.trainingAlternatives = data

        # old approach for fetch data from training_alternatives
        # for l in data:
        #     if l not in CustomModelItem.trainingAlternatives:
        #         CustomModelItem.trainingAlternatives.append(l)
        return True

    @staticmethod
    def fetchNotesFromDatabase(database):
        try:
            data = database.data("training_notes")
        except:
            con = sqlite3.connect(database)
            with con:
                c = con.cursor()
                sqlCommand = "SELECT * FROM training_notes"
                try:
                    c.execute(sqlCommand)
                except sqlite3.OperationalError:
                    return False
                data = c.fetchall()
            con.close()
            data = [list(item) for item in data]

        CustomModelItem.trainingNotes = data

        # old approach for fetch notes from training_notes
        # for l in data:
        #     if l not in CustomModelItem.trainingNotes:
        #         CustomModelItem.trainingNotes.append(l)
        return True

    def setData(self, value, role, defaultPurpose = True):
        if (role == QtCore.Qt.DisplayRole):
            if len(value) != 0:
                self.setUserData(value)
                self.model().itemChanged.emit(self, role, defaultPurpose)
        if (role == QtCore.Qt.EditRole):
            self.setUserData(value)
            self.model().itemChanged.emit(self, role, defaultPurpose)
        super().setData(value, role)
        self.model().itemChanged.emit(self, role, defaultPurpose)

    def setUserData(self, data):
        if not isinstance(data, str):
            if isinstance(data, int):
                data = str(data)
            else:
                raise TypeError(
                        "input <{input_name}> for 'setUserData' does not match {type_name_1}".format(
                                input_name = str(data),
                                type_name_1 = str
                            )
                    )
        self._userData = data

    def type():
        return 1001

    def userData(self):
        return self._userData

class CustomNewTrainingroutineDialog(QtWidgets.QDialog):

    ObjectType = "CustomNewTrainingroutineDialog"
    customDataChanged = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Create a new Trainingroutine")
        self.data = {"exerciseDefaultNumber":0}

        self.toCommit = {"training_routine":None, "training_alternatives":list()}

        # 1: Groups
        self.inputGroup = QtWidgets.QWidget(self)
        self.inputSubGroup1 = QtWidgets.QWidget(self.inputGroup)
        self.inputSubGroup2 = QtWidgets.QWidget(self.inputGroup)
        self.editorGroup = QtWidgets.QWidget(self)
        self.buttonGroup = QtWidgets.QWidget(self)

        # 2: Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.inputLayout = QtWidgets.QHBoxLayout(self.inputGroup)
        self.inputSubLayout1 = QtWidgets.QFormLayout(self.inputSubGroup1)
        self.inputSubLayout2 = QtWidgets.QGridLayout(self.inputSubGroup2)
        self.editorLayout = QtWidgets.QVBoxLayout(self.editorGroup)
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonGroup)

        # 3: Members
        self.nameEdit = QtWidgets.QLineEdit(self.inputSubGroup1)
        self.nameEdit.setPlaceholderText("Enter new Name here...")
        self.numberEdit = CustomSpinBox(self.inputSubGroup1)
        self.numberEdit.setMinimum(0)
        self.numberEdit.setValue(self.data["exerciseDefaultNumber"])
        self.numberEdit.setMaximum(20)
        self.addAlternativeButton = QtWidgets.QPushButton(
                "Add Alternative",
                self.inputSubGroup2
            )
        self.deleteAlternativesButton = QtWidgets.QPushButton(
                "Delete Alternatives",
                self.inputSubGroup2
            )
        self.deleteAlternativesButton.setEnabled(False)
        self.editor = CustomRoutineEditor(parent = self.editorGroup)
        self.alternativeEditor = CustomRoutineEditor(parent = self.editorGroup)
        self.alternativeEditor.setHidden(True)
        self.acceptButton = QtWidgets.QPushButton("OK", self.buttonGroup)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self.buttonGroup)

        # 4: Layout Settings
        self.mainLayout.addWidget(self.inputGroup)
        self.mainLayout.addWidget(self.editorGroup)
        self.mainLayout.addWidget(self.buttonGroup)

        self.inputLayout.setContentsMargins(0,0,0,0)
        self.inputLayout.addWidget(self.inputSubGroup1)
        self.inputLayout.addStretch()
        self.inputLayout.addStretch()
        self.inputLayout.addWidget(self.inputSubGroup2)

        self.inputSubLayout1.setContentsMargins(0,0,0,0)
        self.inputSubLayout1.addRow("Name", self.nameEdit)
        self.inputSubLayout1.addRow("Nuber of Exercises", self.numberEdit)

        self.inputSubLayout2.setContentsMargins(0,0,0,0)
        self.inputSubLayout2.addWidget(self.addAlternativeButton,0,0)
        self.inputSubLayout2.addWidget(self.deleteAlternativesButton,1,0)

        self.editorLayout.setContentsMargins(0,0,0,0)
        self.editorLayout.addWidget(self.editor)
        self.editorLayout.addWidget(self.alternativeEditor)

        self.buttonLayout.setContentsMargins(0,0,0,0)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # 5: PushButton Modality
        self.acceptButton.setEnabled(False)

        # 6: Connections
        self.nameEdit.textEdited.connect(self.onNameEditValueChanged)
        self.numberEdit.valueChanged.connect(self.onExerciseNumChanged)

        self.addAlternativeButton.clicked.connect(self.onAddAlternative)
        self.deleteAlternativesButton.clicked.connect(self.onDeleteAlternatives)

        self.customDataChanged.connect(self.onAlternativeCountChanged)

        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.rejectButton.clicked.connect(self.reject)

        # 7: Help
        self.__setHelp()

        # 8: Window Geometry
        width = self.editor.horizontalHeader().length()
        self.setGeometry(200,100,width,500)

        # 9: Show Dialog
        self.exec()

    def __setHelp(self):
        # Name
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Name for the new Trainingroutine.</b>
        </p>

        <p>
        The Value entered must be a <i>character vector</i> or a <i>string scalar</i>!
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Enter the Name for the new Trainingroutine
        </p>
        """
        self.nameEdit.setWhatsThis(whatsThis)
        self.nameEdit.setToolTip(toolTip)

        # Number of Exercises
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Number of Excercises for the new Trainingroutine.</b>
        </p>

        <p>

        The Value entered must be an <i>integer</i>!
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Enter the Number of Excercises for the new Trainingroutine
        </p>
        """
        self.numberEdit.setWhatsThis(whatsThis)
        self.numberEdit.setToolTip(toolTip)

        # Add Alternative Button
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Add a new Trainingalternative to the current Trainingroutine.</b>
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Add a new Trainingalternative to the current Trainingroutine
        </p>
        """
        self.addAlternativeButton.setWhatsThis(whatsThis)
        self.addAlternativeButton.setToolTip(toolTip)

        # Delete Alternative Button
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Delete an added Trainingalternative.</b>
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Delete an added Trainingalternative
        </p>
        """
        self.deleteAlternativesButton.setWhatsThis(whatsThis)
        self.deleteAlternativesButton.setToolTip(toolTip)

        # Editor
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Editor:</b>
        </p>
        <p>
        The Editor shows the Blueprint for the new Trainingroutine.
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        The Editor shows the Blueprint for the new Trainingroutine
        </p>
        """
        self.editor.setWhatsThis(whatsThis)
        self.editor.setToolTip(toolTip)

    def appendAlternative(self, data):
        model = self.alternativeEditor.model()
        items = [QtGui.QStandardItem(None) for item in range(model.columnCount())]
        for i in range(model.columnCount()):
            if i == 0:
                text = "{num}) {name}".format(num = data[0],
                                              name = data[3]
                                        )
                items[i].setData(text, role = QtCore.Qt.DisplayRole)
            else:
                text = data[3+i]
                items[i].setData(text, role = QtCore.Qt.DisplayRole)
        model.appendRow(items)
        self.alternativeEditor.setHidden(False)

    def deleteAlternatives(self):
        model = self.alternativeEditor.model()
        oldRows = model.rowCount()
        for i in range(model.rowCount(), -1, -1):
            model.removeRow(i)
        self.alternativeEditor.rowCountChanged(oldRows, 0)
        self.alternativeEditor.setHidden(True)
        self.toCommit["training_alternatives"] = []
        self.customDataChanged.emit()

    def onAcceptButtonClicked(self):
        dialogData = [
                self.nameEdit.text(),
                self.numberEdit.value(),
            ]
        model = self.editor.model()
        values = []
        for i in range(self.editor.model().rowCount()):
            l = []
            for n in range(self.editor.model().columnCount()):
                index = self.editor.model().index(i,n)
                item = self.editor.model().item(i,n)
                if n == 0:
                    widget = self.editor.indexWidget(index)
                    text = widget.currentText()
                    l.append(text)
                elif n == model.columnCount()-1:
                    widget = self.editor.indexWidget(index)
                    text = widget.currentText()
                    l.append(text)
                else:
                    text = item.data(role = QtCore.Qt.DisplayRole)
                    l.append(text)
            values.append(l)
        data = {"dialog_data":dialogData,
                "model":model,
                "routine_values":values,
            }
        self.toCommit["training_routine"] = data

    def onAddAlternative(self):
        dialog = CustomAddAlternativeDialog(self)
        if dialog.result():
            data = dialog.toCommit["alternative_values"]
            num = len(self.toCommit["training_alternatives"])
            data.insert(1, str(num+1))
            dialog.toCommit["model"] = self.alternativeEditor.model()
            self.appendAlternative(data)
            self.toCommit["training_alternatives"].append(dialog.toCommit)
            self.customDataChanged.emit()
        else:
            pass

    def onAlternativeCountChanged(self):
        if len(self.toCommit["training_alternatives"]) == 0:
            self.deleteAlternativesButton.setEnabled(False)
        else:
            self.deleteAlternativesButton.setEnabled(True)

    def onDeleteAlternatives(self):
        self.deleteAlternatives()

    def onExerciseNumChanged(self, value):

        oldValue = self.numberEdit.oldValue()
        diff = value-oldValue
        model = self.editor.model()
        if diff < 0:
            for i in range(oldValue, value-1, -1):
                model.removeRow(i)
                self.editor.rowCountChanged(oldValue, value)
        else:
            for i in range(diff):
                items = [QtGui.QStandardItem(None) for item in range(model.columnCount())]
                model.appendRow(items)
            for i in range(oldValue, value+1, 1):
                index = model.index(i, 10)
                comboMode = CustomComboBox(self.editor)
                comboMode.insertItems(0, [], mode = "modes")
                self.editor.setIndexWidget(index, comboMode)

                index = model.index(i, 0)
                comboAlt = CustomComboBox(self.editor)
                comboAlt.insertItems(0, [], mode = "gym")
                self.editor.setIndexWidget(index, comboAlt)

                comboMode.currentTextChanged.connect(
                        comboAlt.onTextChanged
                    )

    def onNameEditValueChanged(self, value):
        if self.nameEdit.text() == "":
            self.acceptButton.setEnabled(False)
        else:
            self.acceptButton.setEnabled(True)

class CustomRoutineEditor(QtWidgets.QTableView):

    ObjectType = "CustomRoutineEditor"

    wheelTurned = QtCore.pyqtSignal(QtCore.QObject, QtGui.QWheelEvent)
    rowHasBeenMoved = QtCore.pyqtSignal(int, int)

    def __init__(self, parent = None, modelRows = 0, modelColumns = 10,
                 headerLabels = None, database = None, rowsMovable = False):

        super().__init__(parent)
        self._modelRows = None
        self._modelColumns = None
        self._headerLabels = None
        self._database = None

        self.setModelRows(modelRows)
        self.setModelColumns(modelColumns)
        self.setHeaderLabels(headerLabels)
        self.setDatabase(database)

        self.__model = QtGui.QStandardItemModel(modelRows, modelColumns, self)
        self.__setHorizontalHeaderLabels()
        self.verticalHeader().setSectionsMovable(rowsMovable)
        self.verticalHeader().sectionMoved.connect(self.onSectionMoved)
        self.setModel(self.model())
        self.setColumnResizeMode()

    def __setHorizontalHeaderLabels(self):
        if self.headerLabels():
            labels = self.headerLabels()
        else:
            if self.modelColumns() != 10:
                labels = ["Column {}".format(i) for i in range(self.modelColumns())]
            else:
                labels = (
                        ["Excercise",
                        "Sets",
                        "Reps",
                        "Warm Up",
                        "Week 1",
                        "Week 2",
                        "Week 3",
                        "Week 4",
                        "Week 5",
                        "Week 6",
                        "Mode"]
                    )
        self.model().setHorizontalHeaderLabels(labels)

    def setColumnResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def database(self):
        return self._database

    def eventFilter(self, obj, event):
        if isinstance(event, QtGui.QWheelEvent):
            self.wheelTurned.emit(self, event)
            return True
        return super().eventFilter(obj, event)

    def headerLabels(self):
        return self._headerLabels

    def model(self):
        return self.__model

    def modelColumns(self):
        return self._modelColumns

    def modelRows(self):
        return self._modelRows

    def onSectionMoved(self, sectionIndex, fromIndex, toIndex):
        self.rowHasBeenMoved.emit(fromIndex, toIndex)

    def resizeColumnToContent(self, column):
        header = self.horizontalHeader()
        columnWidths = [header.sectionSize(i) for i in range(header.count())]
        maxWidth = max(columnWidths)
        self.setColumnWidth(column, maxWidth*2)

    def setDatabase(self, database):
        self._database = database

    def setHeaderLabels(self, labels):
        self._headerLabels = labels

    def setModelColumns(self, count):
        self._modelColumns = count

    def setModelRows(self, count):
        self._modelRows = count

class CustomScrollArea(QtWidgets.QScrollArea):

    ObjectType = "CustomScrollArea"

    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setWidgetResizable(True)

class CustomSpinBox(QtWidgets.QSpinBox):

    def __init__(self, *args):
        super().__init__(*args)
        self.__oldValue = None
        self.setKeyboardTracking(False)

    def keyPressEvent(self, event):
        self.setOldValue(self.value())
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self.setOldValue(self.value())
        super().mousePressEvent(event)

    def oldValue(self):
        return self.__oldValue

    def setOldValue(self, value):
        self.__oldValue = value

    def wheelEvent(self, event):
        self.setOldValue(self.value())
        super().wheelEvent(event)

class CustomStandardEditorWidget(QtWidgets.QWidget):

    def __init__(self, message, parent = None):
        super().__init__(parent)
        self.message = message
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAutoFillBackground(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.edit = QtWidgets.QLineEdit("Enter new Value", self)

        canvas = CreateCanvas(
                self.message,
                fontSize = 11,
            )
        pixmap = CreateQPixmap(canvas)
        self.label.setPixmap(pixmap)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

class CustomWidget(QtWidgets.QWidget):

    ObjectType = "CustomWidget"

    def __init__(self, *args):
        super().__init__(*args)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("""

        CustomWidget {
            background-color: rgba(255,255,255,0%);
        }

        """)

class ExceptionHandler():

    def displayException(self, exceptionType, value, traceBack):
        string = "Traceback: {traceback} \n Exception Type: {etype} \n Value: {value}".format(
                traceback = traceBack,
                etype = exceptionType,
                value = str(value)
            )
        print(string)

    def handleException(self, debugging = False):
        if not debugging:
            return False

        etype, value, traceBack = sys.exc_info()
        self.displayException(etype, value, traceBack)


if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            super().__init__(*args)

            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Dialog Test")
            self.show()

            self.dialog = CustomNewTrainingroutineDialog(self)
            if self.dialog.result():
                dbCreator = database("database")
                dbName = self.dialog.toCommit["training_routine"]["dialog_data"][0]
                values = self.dialog.toCommit["training_routine"]["routine_values"]
                columnNames = ( ("exercise", "TEXT"),
                                ("sets", "TEXT"),
                                ("repetitions", "TEXT"),
                                ("warm_up", "TEXT"),
                                ("week_1", "TEXT"),
                                ("week_2", "TEXT"),
                                ("week_3", "TEXT"),
                                ("week_4", "TEXT"),
                                ("week_5", "TEXT"),
                                ("week_6", "TEXT"),
                                ("mode", "TEXT"),
                            )
                dbCreator.createTable(dbName,
                                      "training_routine",
                                      columnNames
                                      )
                for i in range(len(values)):
                    insert = values[i]
                    dbCreator.addEntry(dbName,
                                       "training_routine",
                                       insert)

                columnNames = (
                        ("exerciseID", "INT"),
                        ("label", "TEXT"),
                        ("short", "TEXT"),
                        ("alternative", "TEXT"),
                        ("sets", "TEXT"),
                        ("repetitions", "TEXT"),
                        ("warm_up", "TEXT"),
                        ("week_1", "TEXT"),
                        ("week_2", "TEXT"),
                        ("week_3", "TEXT"),
                        ("week_4", "TEXT"),
                        ("week_5", "TEXT"),
                        ("week_6", "TEXT"),
                        ("mode", "TEXT"),
                    )
                dbCreator.createTable(dbName,
                                      "training_alternatives",
                                      columnNames
                                      )

                for i in range(len(self.dialog.toCommit["training_alternatives"])):
                    data = self.dialog.toCommit["training_alternatives"][i]["alternative_values"]
                    insert = data
                    dbCreator.addEntry(dbName,
                                       "training_alternatives",
                                       insert)

                columnNames = (
                        ("exerciseID", "INT"),
                        ("label", "TEXT"),
                        ("short", "TEXT"),
                        ("note", "TEXT")
                    )
                dbCreator.createTable(dbName,
                                      "training_notes",
                                      columnNames
                                      )

                sys.exit()
            else:
                sys.exit()


    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())