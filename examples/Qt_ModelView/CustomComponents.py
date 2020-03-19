# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3
import string

from PyQt5 import QtWidgets, QtCore, QtGui

class CustomBoxLayout(QtWidgets.QBoxLayout):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.setSizeConstraint(QtWidgets.QBoxLayout.SetMinimumSize)
        
class CustomScrollArea(QtWidgets.QScrollArea):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

class CustomModelItem(QtGui.QStandardItem):
    
    def __init__(self, displayData, *args):
        super().__init__(*args)
        self.displayData = displayData
        self.trainingAlternatives = list()
        self.trainingNotes = list()
        self.lowercaseLetters = string.ascii_lowercase                
        
    def fetchAlternativesFromDatabase(self, database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_alternatives"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        data = [list(item) for item in data]
        self.trainingAlternatives.extend(data)
            
    def fetchNotesFromDatabase(self, database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_notes"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        data = [list(item) for item in data]
        self.trainingNotes.extend(data)
    
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
                Warm Up TEXT,
                Repetition TEXT,
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
            values = "?, " * len(self.trainingAlternatives[0])
            values = values[:-2]
            sqlCommand = "INSERT INTO {name} VALUES({values})".format(
                    name = table,
                    values = values,
                )
            c.executemany(sqlCommand, self.trainingAlternatives)
            
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
            values = "?, " * len(self.trainingNotes[0])
            values = values[:-2]
            sqlCommand = "INSERT INTO {name} VALUES({values})".format(
                    name = table,
                    values = values,
                )
            c.executemany(sqlCommand, self.trainingNotes)
            
        con.close()
        
    def addTrainingAlternative(self, exerciseID, alternativeExercise, warmUp, repetition,
                               w1, w2, w3, w4, w5, w6, 
                               alternativeID = None, label = None, short = None):
        if not alternativeID:
            alternativeID = len(self.trainingAlternatives) + 1
        
        if not label:
            label = "{num}".format(num = str(len(self.trainingAlternatives) + 1))
            
        if not short:
            short = "alternative {num}".format(num = str(len(self.trainingAlternatives) + 1))
            
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
        self.trainingAlternatives.append(data)
    
    def deleteTrainingAlternativ(self, index):
            try:
                del self.trainingAlternatives[index]
            except IndexError:
                return
    
    def addTrainingNote(self, note, noteID = None, label = None, short = None):
        if not noteID:
            noteID = len(self.trainingNotes) + 1
            
        if not label:
            label = self.lowercaseLetters[len(self.trainingNotes)]
            
        if not short:
            short = "note {num}".format(num = str(len(self.trainingNotes) + 1))
            
        data = [
                noteID,
                label,
                short,
                note,
            ]
        self.trainingNotes.append(data)
        
    def deleteTrainingNote(self, index):
        try:
            del self.trainingNotes[index]
        except IndexError:
            return

if __name__ == "__main__":
    
    item = CustomModelItem("test")
    item.fetchAlternativesFromDatabase("database/test_database.db")
    item.fetchNotesFromDatabase("database/test_database.db")
    