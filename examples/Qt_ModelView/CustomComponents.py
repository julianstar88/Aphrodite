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
        for item in data:
            alternative = {}
            alternative["id"] = item[0]
            alternative["exerciseID"] = item[1]
            alternative["label"] = item[2]
            alternative["short"] = item[3]
            alternative["alternativeExercise"] = item[4]
            alternative["warmUp"] = item[5]
            alternative["repetition"] = item[6]
            alternative["w1"] = item[7]
            alternative["w2"] = item[8]
            alternative["w3"] = item[9]
            alternative["w4"] = item[10]
            alternative["w5"] = item[11]
            alternative["w6"] = item[12]
            self.trainingAlternatives.append(alternative)
            
    def fetchNotesFromDatabase(self, database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            sqlCommand = "SELECT * FROM training_notes"
            c.execute(sqlCommand)
            data = c.fetchall()
        con.close()
        for item in data:
            note = {}
            note["id"] = item[0]
            note["label"] = item[1]
            note["short"] = item[2]
            note["note"] = item[3]
            self.trainingNotes.append(note)
    
    def commitAlternativesToDatabase(self, database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            
            # 1: delete the old talbe as it is no longer important
            sqlCommand = "DROP TABLE IF EXISTS training_alternatives"
            c.execute(sqlCommand)
            
            # 2: recreate the table with new values
            
            
        
    def commitNotesToDatabase(self, database):
        con = sqlite3.connect(database)
        with con:
            c = con.cursor()
            
            sqlCommand = "SELECT * FROM training_notes)"
            c.execute(sqlCommand)
            columns = [item[0] for item in c.description]
            
            # sqlCommand = "DROP TABLE IF EXISTS training_notes"
            # c.execute(sqlCommand)
        con.close()
        return columns
        
    def addTrainingAlternative(self, exerciseID, alternativeExercise, warmUp, repetition,
                               w1, w2, w3, w4, w5, w6, 
                               alternativeID = None, label = None, short = None):
        if not alternativeID:
            alternativeID = len(self.trainingAlternatives)
        
        if not label:
            label = "{num}".format(num = str(len(self.trainingAlternatives)))
            
        if not short:
            short = "alternative {num}".format(num = str(len(self.trainingAlternatives)))
            
        alternative = {}
        alternative["id"] = alternativeID
        alternative["exerciseID"] = exerciseID
        alternative["label"] = label
        alternative["short"] = short
        alternative["alternativeExercise"] = alternativeExercise
        alternative["warmUp"] = warmUp
        alternative["repetition"] = repetition
        alternative["w1"] = w1
        alternative["w2"] = w2
        alternative["w3"] = w3
        alternative["w4"] = w4
        alternative["w5"] = w5
        alternative["w6"] = w6
        self.trainingAlternatives.append(alternative)
    
    def deleteTrainingAlternativ(self, key, value):
        for item in self.trainingAlternatives:
            try:
                if item[key] == value:
                    index = self.trainingAlternatives.index(item)
                    del self.trainingAlternatives[index]
            except KeyError:
                continue
    
    def addTrainingNote(self, note, noteID = None, label = None, short = None):
        if not noteID:
            noteID = len(self.trainingNotes)
            
        if not label:
            label = self.lowercaseLetters[len(self.trainingNotes)]
            
        if not short:
            short = "note {num}".format(num = str(len(self.trainingNotes)))
            
        note = {}
        note["id"] = noteID
        note["label"] = label
        note["short"] = short
        note["note"] = note
        self.trainingNotes.append(note)
        
    def deleteTrainingNote(self, key, value):
        for item in self.trainingNotes:
            try:
                if item[key] == value:
                    index = self.trainingNotes.index(item)
                    del self.trainingNotes[index]
            except KeyError:
                continue

if __name__ == "__main__":
    item = CustomModelItem("test")
    item.fetchAlternativesFromDatabase("database/test_database.db")
    item.fetchNotesFromDatabase("database/test_database.db")
    
    oldNotes = item.trainingNotes
    
    test = item.commitNotesToDatabase("database/test_database.db")
        