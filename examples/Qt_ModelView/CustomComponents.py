# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string
import sys

from PyQt5 import QtWidgets, QtCore, QtGui

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

class CustomExerciseEditorWidget(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)
        self.alternativeGroup = QtWidgets.QGroupBox("Alternatives", self)
        self.noteGroup = QtWidgets.QGroupBox("Notes", self)
        self.buttonGroup = QtWidgets.QGroupBox(self)

        self.alternativeEdit = QtWidgets.QLineEdit("Add Trainingalternatives", self)
        self.noteEdit = QtWidgets.QLineEdit("Add Trainingnotes", self)
        self.doneButton = QtWidgets.QPushButton("Done", self)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.alternativeLayout = QtWidgets.QVBoxLayout(self.alternativeGroup)
        self.noteLayout = QtWidgets.QVBoxLayout(self.noteGroup)
        self.buttonLayout = QtWidgets.QHBoxLayout(self.buttonGroup)

        self.vspacer = QtWidgets.QSpacerItem(0, 50)
        self.hspacer = QtWidgets.QSpacerItem(300, 0)

        self.mainLayout.addWidget(self.alternativeGroup)
        self.mainLayout.addWidget(self.alternativeEdit)
        self.mainLayout.addSpacerItem(self.vspacer)
        self.mainLayout.addWidget(self.noteGroup)
        self.mainLayout.addWidget(self.noteEdit)
        self.mainLayout.addWidget(self.buttonGroup)
        self.mainLayout.addSpacerItem(self.hspacer)

        for i in range(3):
            string = "Trainingalternative" + " " + str(i)
            self.alternativeLayout.addWidget(QtWidgets.QLabel(string,
                                          self.alternativeGroup))

            string = "Trainingnote" + " " + str(i)
            self.noteLayout.addWidget(QtWidgets.QLabel(string,
                                           self.noteGroup))

        self.buttonLayout.addSpacerItem(QtWidgets.QSpacerItem(250, 0,
                                            QtWidgets.QSizePolicy.MinimumExpanding))
        self.buttonLayout.addWidget(self.doneButton)

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
                id INT,
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
                        id INT,
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
            # self.t = CustomExerciseEditorWidget(self)

            # self.setCentralWidget(self.t)
            # self.show()
            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Dialog Test")
            self.show()

            self.dialog = CustomExerciseEditorWidget(self)
            self.dialog.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())