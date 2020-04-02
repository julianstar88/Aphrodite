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
        self.rejectButton = QtWidgets.QPushButton("Cancel", self.buttonGroup)
        self.exerciseIdEdit = QtWidgets.QLineEdit(self.alternativeGroup)
        self.exerciseIdEdit.setPlaceholderText("New Exercise ID...")
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
                alternativeID,
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

    def addTrainingNote(self, note, noteID = None, label = None, short = None):
        if not noteID:
            noteID = len(type(self).trainingNotes) + 1

        if not label:
            label = type(self).lowercaseLetters[len(type(self).trainingNotes)]

        if not short:
            short = "note {num}".format(num = str(len(type(self).trainingNotes) + 1))

        data = [
                noteID,
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
                Repititions TEXT,
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

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Create a new Trainingroutine")

        # 1: Groups
        self.inputGroup = QtWidgets.QWidget(self)
        self.editorGroup = QtWidgets.QWidget(self)
        self.buttonGroup = QtWidgets.QWidget(self)

        # 2: Layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.inputLayout = QtWidgets.QFormLayout(self.inputGroup)
        self.editorLayout = QtWidgets.QVBoxLayout(self.editorGroup)
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonGroup)

        # 3: Members
        self.nameEdit = QtWidgets.QLineEdit(self.inputGroup)
        self.modeEdit = QtWidgets.QComboBox(self.inputGroup)
        self.numberEdit = QtWidgets.QSpinBox(self.inputGroup)
        self.numberEdit.setMinimum(0)
        self.numberEdit.setMaximum(20)
        self.editor = GraphicalRoutineEditor(parent = self.editorGroup)
        self.acceptButton = QtWidgets.QPushButton("OK", self.buttonGroup)
        self.acceptButton.setDefault(True)
        self.rejectButton = QtWidgets.QPushButton("Cancel", self.buttonGroup)

        # 4: Layout Settings
        self.mainLayout.addWidget(self.inputGroup)
        self.mainLayout.addWidget(self.editorGroup)
        self.mainLayout.addWidget(self.buttonGroup)

        self.inputLayout.setContentsMargins(0,0,0,0)
        self.inputLayout.addRow("Name", self.nameEdit)
        self.inputLayout.addRow("Trainingmode", self.modeEdit)
        self.inputLayout.addRow("Nuber of Exercises", self.numberEdit)

        self.editorLayout.setContentsMargins(0,0,0,0)
        self.editorLayout.addWidget(self.editor)

        self.buttonLayout.setContentsMargins(0,0,0,0)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.acceptButton)
        self.buttonLayout.addWidget(self.rejectButton)

        # 5: Connections
        self.numberEdit.valueChanged.connect(self.onExerciseNumChanged)

        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)

        # 6: Help

        # 7: Show Help
        self.exec()

    def onExerciseNumChanged(self, value):
        pass

class CustomScrollArea(QtWidgets.QScrollArea):

    ObjectType = "CustomScrollArea"

    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setWidgetResizable(True)

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
                sys.exit()
            else:
                sys.exit()


    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())