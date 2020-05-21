# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string
import sys

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

class CustomAddNoteDialog(QtWidgets.QDialog):

    ObjectType = "CustomAddNoteDialog"

    def __init__(self, *args):
        super().__init__(*args)

        # 1: Groups
        self.noteGroup = QtWidgets.QWidget(self)
        self.buttonGroup = QtWidgets.QWidget(self)

        # 2: Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.noteLayout = QtWidgets.QFormLayout(self.noteGroup)
        self.noteLayout.setContentsMargins(0,0,0,0)
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonGroup)
        self.buttonLayout.setContentsMargins(0,0,0,0)

        # 3: Members
        self.exerciseIdEdit = QtWidgets.QLineEdit(self.noteGroup)
        self.exerciseIdEdit.setPlaceholderText("New Exercise ID...")
        self.shortNameEdit = QtWidgets.QLineEdit(self.noteGroup)
        self.shortNameEdit.setPlaceholderText("New Shrot Name...")
        self.descriptionEdit = QtWidgets.QTextEdit(self.noteGroup)
        self.descriptionEdit.setPlaceholderText("Enter Description of Trainingnote here...")
        self.acceptButton = QtWidgets.QPushButton("OK", self.buttonGroup)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self.buttonGroup)

        # 4: Layout Settings
        self.mainLayout.addWidget(self.noteGroup)
        self.mainLayout.addWidget(self.buttonGroup)

        self.noteLayout.addRow("Exercise ID:", self.exerciseIdEdit)
        self.noteLayout.addRow("Short Name:", self.shortNameEdit)
        self.noteLayout.addRow("Description:", self.descriptionEdit)

        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # 5: Connections
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)

        # 6: Help
        self.__setHelp()

        # 7: Show Dialog
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
            <b>Enter the Exercise ID for the new Trainingnote.</b>
        </p>

        <p>
        The Exercise ID is a unique Number specifying to which Exercise this
        Note belongs. The new Note (as well as a generated subscript)
        will be added to the Trainingroutine. The Value entered must be a <i>integer</i>!
        </p>
        """

        toolTip = """
        <p style='text-align:left;'>
        Enter the Exercise ID for the new Trainingnote
        </p>
        """
        self.exerciseIdEdit.setWhatsThis(whatsThis)
        self.exerciseIdEdit.setToolTip(toolTip)

        # Short Name
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </stlye>
        </head>

        <p>
            <b>Enter the Short Name for the new Trainingnote.</b>
        </p>

        <p>
        The purpose of the Short Name is to be displayed, whenever a summary of
        all Notes is neccessary (e.g. if if a note should be deleted via the
        <i>Delete Trainingnote...</i> Dialog). The entered Value can be a
        <i>character vector</i> or a <i>string scalar</i>.
        </p>
        """
        toolTip = """
        <p style='text-align:left;'>
        Enter the Short Name for the new Trainingnote.
        </p>
        """
        self.shortNameEdit.setWhatsThis(whatsThis)
        self.shortNameEdit.setToolTip(toolTip)

        # Description
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Description for the new Trainingnote.</b>
        </p>

        <p>
        The Description shows in detail, whats meant with the new Trainingnote.
        It gets displayed on the left pane if a Trainingroutine has been opened
        and is linked to the corresponding Exercise via an unique Label.The entered Value
        can be a <i>character vector</i> or a <i>string scalar</i>.
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Enter the Description for the new Trainingnote.
        </p>
        """
        self.descriptionEdit.setWhatsThis(whatsThis)
        self.descriptionEdit.setToolTip(toolTip)

class CustomBoxLayout(QtWidgets.QBoxLayout):

    ObjectType = "CustomBoxLayout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeConstraint(QtWidgets.QBoxLayout.SetMinAndMaxSize)

class CustomComboBox(QtWidgets.QComboBox):

    ObjectType = "CustomComboBox"

    def __init__(self, *args):
        super().__init__(*args)
        self.text = {
                "exercises_gym":[
                        "Bankdrücken KH",
                        "Bankdürcken LH",
                        "Klimmzüge",
                        "Kniebeugen",
                        "Seitenheben KH",
                        "Seitenheben M",
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


class CustomDeleteAlternativeDialog(QtWidgets.QDialog):

    # TODO: Implement the Delete Functionality

    def __init__(self, *args):
        super().__init__(*args)

class CustomDeleteNoteDialog(QtWidgets.QDialog):

    # TODO: Implement the Delete Functionality

    def __init__(self, *args):
        super().__init__(*args)

class CustomEventFilter(QtCore.QObject):

    def __init__(self, *args):
        super().__init__(*args)


    def eventFilter(self, obj, event):
        print(event.type())
        return False

class CustomLabel(QtWidgets.QLabel):

    ObjectType = "CustomLabel"

    def __init__(self, QPixmap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = None
        self.setPixmap(QPixmap)
        self.setAutoFillBackground(False)

class CustomModelItem(QtGui.QStandardItem):

    ObjectType = "CustomModelItem"

    trainingAlternatives = list()
    trainingNotes = list()
    lowercaseLetters = string.ascii_lowercase

    def __init__(self, displayData, *args, **kwargs):
        super().__init__(displayData, *args, **kwargs)
        self.setUserData(displayData)

    def addTrainingAlternative(self, exerciseID, alternativeExercise, warmUp, repetition,
                               w1, w2, w3, w4, w5, w6,
                               alternativeID = None, label = None, short = None):
        if not alternativeID:
            alternativeID = len(type(self).trainingAlternatives) + 1

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
        for l in data:
            if l not in CustomModelItem.trainingAlternatives:
                CustomModelItem.trainingAlternatives.append(l)
        return True

    @staticmethod
    def fetchNotesFromDatabase(database):
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
        for l in data:
            if l not in CustomModelItem.trainingNotes:
                CustomModelItem.trainingNotes.append(l)

    def setData(self, value, role, defaultPurpose = True):
        if role == QtCore.Qt.DisplayData:
            self.setUserData(value)
        super().setData(value, role)
        self.model().itemChanged.emit(self, defaultPurpose)

    def setUserData(self, data):
        if not type(data) == str:
            raise TypeError(
                    "input <{input_name}> for 'setDisplayData' does not match {type_name}".format(
                            input_name = str(data),
                            type_name = str
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = QtGui.QStandardItemModel(0, 10, self)
        self.__model.setHorizontalHeaderLabels(["Excercise",
                                              "Sets",
                                              "Reps",
                                              "Warm Up",
                                              "Week 1",
                                              "Week 2",
                                              "Week 3",
                                              "Week 4",
                                              "Week 5",
                                              "Week 6",
                                              "Mode"])
        self.setModel(self.model())
        self.setColumnResizeMode()

    def setColumnResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def model(self):
        return self.__model

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
                fontSize = 9,
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