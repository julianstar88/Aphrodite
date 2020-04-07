# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string
import sys

from HelperModules import GraphicalRoutineEditor

from PyQt5 import QtWidgets, QtCore, QtGui

class CustomAddAlternativeDialog(QtWidgets.QDialog):

    ObjectType = "CustomAddAlternativeDialog"

    def __init__(self, *args):
        super().__init__(*args)

        # 1: Groups
        self.alternativeGroup = QtWidgets.QWidget(self)
        self.buttonGroup = QtWidgets.QWidget(self)

        # 2: Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.alternativeLayout = QtWidgets.QFormLayout(self.alternativeGroup)
        self.alternativeLayout.setContentsMargins(0,0,0,10)
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
        self.longNameEdit = QtWidgets.QLineEdit(self.alternativeGroup)
        self.longNameEdit.setPlaceholderText("New Long Name...")

        # 4: Layout Settings
        self.mainLayout.addWidget(self.alternativeGroup)
        self.mainLayout.addWidget(self.buttonGroup)

        self.alternativeLayout.addRow("Exercise ID:", self.exerciseIdEdit)
        self.alternativeLayout.addRow("Short Name:", self.shortNameEdit)
        self.alternativeLayout.addRow("Long Name:", self.longNameEdit)

        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # 5: Connectios
        self.exerciseIdEdit.textEdited.connect(self.onExerciseIdChanged)

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

        # Long Name
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Enter the Long Name for the new Trainingalternative.</b>
        </p>

        <p>
        The Long Name of a Trainingaltervative is the Name, which is will be displayed
        directly below of the Trainingroutine. The entered Value can ba a
        <i>chacter vector</i> or a <i>string scalar</i>.
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Enter the Long Name for the new Trainingalternative
        </p>
        """
        self.longNameEdit.setWhatsThis(whatsThis)
        self.longNameEdit.setToolTip(toolTip)

    def onExerciseIdChanged(self, value):
        if self.exerciseIdEdit.text() == "":
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
        self.displayData = displayData

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
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        data = [list(item) for item in data]
        for l in data:
            if l not in CustomModelItem.trainingAlternatives:
                CustomModelItem.trainingAlternatives.append(l)

    @staticmethod
    def fetchNotesFromDatabase(database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_notes"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        data = [list(item) for item in data]
        for l in data:
            if l not in CustomModelItem.trainingNotes:
                CustomModelItem.trainingNotes.append(l)

    def setData(self, value, role, defaultPurpose = True):
        super().setData(value, role)
        self.model().itemChanged.emit(self, defaultPurpose)

    def type():
        return 1001

class CustomNewTrainingroutineDialog(QtWidgets.QDialog):

    ObjectType = "CustomNewTrainingroutineDialog"
    customDataChanged = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Create a new Trainingroutine")
        self.data = {"exerciseDefaultNumber":0,
                     "exercises":[
                             None,
                             "Bankdürcken",
                             "Klimmzüge",
                             "Kniebeugen",
                             "Seitenheben",
                         ],
                     "modes":[
                             "Gym",
                             "Running",
                         ]
                     }
        self.toCommit = {"routine":None, "alternatives":list()}

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
        self.modeEdit = QtWidgets.QComboBox(self.inputSubGroup1)
        self.modeEdit.insertItems(0,self.data["modes"])
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
        self.editor = GraphicalRoutineEditor(parent = self.editorGroup)
        self.alternativeEditor = GraphicalRoutineEditor(parent = self.editorGroup)
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
        self.inputLayout.addWidget(self.inputSubGroup2)

        self.inputSubLayout1.setContentsMargins(0,0,0,0)
        self.inputSubLayout1.addRow("Name", self.nameEdit)
        self.inputSubLayout1.addRow("Trainingmode", self.modeEdit)
        self.inputSubLayout1.addRow("Nuber of Exercises", self.numberEdit)

        self.inputSubLayout2.setContentsMargins(0,0,0,0)
        self.inputSubLayout2.addWidget(self.addAlternativeButton,0,0)
        self.inputSubLayout2.addWidget(self.deleteAlternativesButton,1,0)
        self.inputSubLayout2.addItem(
                QtWidgets.QSpacerItem(
                        0,self.addAlternativeButton.sizeHint().height(),
                        QtWidgets.QSizePolicy.Minimum,
                        QtWidgets.QSizePolicy.Minimum
                    ),
                2,0
            )

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
        self.rejectButton.clicked.connect(self.reject)

        # 7: Help
        self.__setHelp()

        # 8: Window Geometry
        # width = self.editor.horizontalHeader().length()
        # self.setGeometry(200,100,width,500)
        self.setGeometry(200,100,800,500)

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

        # Training Mode
        whatsThis = """
        <head>
        <style>
            p {text-align:left}
        </style>
        </head>

        <p>
            <b>Set the appropriate Training Mode.</b>
        </p>

        <p>
        At This time only the Gym mode is supported.
        </p>
        """
        toolTip = """
        <p style='text-align:left'>
        Set the appropraite Training Mode
        </p>
        """
        self.modeEdit.setWhatsThis(whatsThis)
        self.modeEdit.setToolTip(toolTip)

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
        text = "{num}) {name}".format(num = data[0], name = data[2])
        items[0].setData(text, role = QtCore.Qt.DisplayRole)
        model.appendRow(items)
        self.alternativeEditor.setHidden(False)

    def deleteAlternatives(self):
        model = self.alternativeEditor.model()
        oldRows = model.rowCount()
        for i in range(model.rowCount()):
            model.removeRow(i)
        self.alternativeEditor.rowCountChanged(oldRows, 0)
        self.alternativeEditor.setHidden(True)
        self.toCommit["alternatives"] = []
        self.customDataChanged.emit()


    def onAddAlternative(self):
        dialog = CustomAddAlternativeDialog(self)
        if dialog.result():
            data = [
                    eval(dialog.exerciseIdEdit.text()),
                    dialog.shortNameEdit.text(),
                    dialog.longNameEdit.text()
                ]
            self.appendAlternative(data)
            self.toCommit["alternatives"].append(data)
            self.customDataChanged.emit()
        else:
            pass

    def onAlternativeCountChanged(self):
        if len(self.toCommit["alternatives"]) == 0:
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
                index = model.index(i, 0)
                combo = QtWidgets.QComboBox(self.editor)
                combo.insertItems(0, self.data["exercises"])
                self.editor.setIndexWidget(index, combo)

    def onNameEditValueChanged(self, value):
        if self.nameEdit.text() == "":
            self.acceptButton.setEnabled(False)
        else:
            self.acceptButton.setEnabled(True)

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
        self.label = QtWidgets.QLabel(self.message, self)
        self.edit = QtWidgets.QLineEdit("Enter new Value", self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

class CustomWidget(QtWidgets.QWidget):

    ObjectType = "CustomWidget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                data = [
                        self.dialog.nameEdit.text(),
                        self.dialog.modeEdit.currentText(),
                        self.dialog.numberEdit.value(),
                        self.dialog.editor.model()
                    ]
                self.dialog.toCommit["routine"] = data
                print(self.dialog.toCommit)
            else:
                sys.exit()


    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())