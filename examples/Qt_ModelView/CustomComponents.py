# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:57:11 2020

@author: Julian
"""
import sqlite3

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
        
        
    def fetchAlternatives(self, database):
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
        
    def commit(self, database):
        pass

if __name__ == "__main__":
    item = CustomModelItem("test")
    item.fetchAlternatives("database/test_database.db")
        
        