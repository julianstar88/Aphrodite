# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string

from PyQt5 import QtWidgets, QtCore, QtGui

class CustomBoxLayout(QtWidgets.QBoxLayout):

    ObjectType = "CustomBoxLayout"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeConstraint(QtWidgets.QBoxLayout.SetMinAndMaxSize)

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

class standardEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAutoFillBackground(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("test:", self)
        self.edit = QtWidgets.QLineEdit("Enter test message", self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

if __name__ == "__main__":

    item = CustomModelItem("test")
    item.fetchAlternativesFromDatabase("database/test_database.db")
    item.fetchNotesFromDatabase("database/test_database.db")
