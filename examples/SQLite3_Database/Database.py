# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:53:18 2020

@author: Julian
"""

import sqlite3 as lite
import os, os.path

class database():
    """
    Create a SQlite3 database file with the name 'databaseName'.

    Input parameter:
        - databaseName: name of the generated database-file type: str
        - tableName: name of the table within a database-file type: str
        - columnNames: name and type of the colums in form of an tupel
            (("name", "type"), ("name", "type"),...)

    Output:
        - A db-file named 'databaseName'
    """
    def __init__(self, path = None, extension = ".db"):
        self.__path = path
        self.__extension = extension
        self.__checkPath()

    def __checkPath(self):
        if self.__path == None:
            self.__path = os.getcwd()
        else:
            npath = os.path.normpath(self.__path)
            self.__path = npath

    def __closeConnection(self, connectionObject):
        connectionObject.close()

    def __establishConnection(self, databaseName):
        databaseName = databaseName + self.__extension
        database = os.path.join(self.__path, databaseName)
        return lite.connect(database)

    def addEntry(self, databaseName, tableName, insert):

        # establish connection
        con = self.__establishConnection(databaseName)

        # do work
        with con:
            c = con.cursor()
            values = '?, ' * len(insert)
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = tableName, values = values)
            c.execute(sql_command, insert)

        # close connection
        self.__closeConnection(con)

    def addManyEntries(self, databaseName, tableName, insert):

        # establish connection
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            values = '?, ' * len(insert[0])
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = tableName, values = values)
            c.executemany(sql_command, insert)

        # close connection
        self.__closeConnection(con)

    def createDatabase(self, databaseName):
        self.__establishConnection(databaseName)

    def createTable(self, databaseName, tableName, columnNames):
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            c.execute("DROP TABLE IF EXISTS {name}".format(name = tableName))
            valueString = ""
            for name in columnNames:
                valueString += "{} {}, ".format(name[0], name[1])
            valueString = valueString[:-2]
            sql_command = "CREATE TABLE {name}({values})".format(name = tableName,
                                                                 values = valueString)
            c.execute(sql_command)
        self.__closeConnection(con)

    def deleteAllEntries(self, databaseName, tableName):

        # establish connection
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name}".format(name = tableName)
            c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def deleteEntry(self, databaseName, tableName, row_id):

        # establish connection
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                name = tableName, row_id = row_id)
            c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def deleteManyEntries(self, databaseName, tableName, row_id_list):

        # establish connection
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            for idx in row_id_list:
                sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                    name = tableName, row_id = idx)
                c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def data(self, databaseName, tableName):

        # establish connection
        con = self.__establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "SELECT * FROM {name}".format(name = tableName)
            c.execute(sql_command)
            data = c.fetchall()

        # close connection
        self.__closeConnection(con)

        return data

    def extension(self):
        return self.__extension

    def path(self):
        return self.__path

    def setExtension(self, extension):
        self.__extension = extension

    def setPath(self, path):
        npath = os.path.normpath(path)
        self.__path = npath

if __name__ == '__main__':

    # create database
    path = r"C:\Users\Julian\Documents\Python\Projekte\Aphrodite\examples\Qt_ModelView\database"
    db = database(path)
    dbName = "test_database_2"

    columnNames = ( ("Exercise", "TEXT"),
                    ("Sets", "TEXT"),
                    ("Repetitions", "TEXT"),
                    ("Warm_Up", "TEXT"),
                    ("Week_1", "TEXT"),
                    ("Week_2", "TEXT"),
                    ("Week_3", "TEXT"),
                    ("Week_4", "TEXT"),
                    ("Week_5", "TEXT"),
                    ("Week_6", "TEXT"),
                    ("mode", "TEXT"),
                )
    db.createTable(dbName, "training_routine", columnNames)

    columnNames = (("exerciseID", "INT"),
                   ("label", "TEXT"),
                   ("short", "TEXT"),
                   ("alternative", "TEXT"),
                   ("Sets", "TEXT"),
                   ("Repetitions", "TEXT"),
                   ("Warm_Up", "TEXT"),
                   ("Week_1", "TEXT"),
                   ("Week_2", "TEXT"),
                   ("Week_3", "TEXT"),
                   ("Week_4", "TEXT"),
                   ("Week_5", "TEXT"),
                   ("Week_6", "TEXT"),
                   ("mode", "TEXT"),
                  )
    db.createTable(dbName, "training_alternatives", columnNames)


    columnNames = (("excerciseID", "INT"),
                   ("label", "TEXT"),
                   ("short", "TEXT"),
                   ("note", "TEXT"))
    db.createTable(dbName, "training_notes", columnNames)


    training = [
        ["Bankdrücken KH", "4", "RBD", "WBD", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6", "gym"],
        ["Klimmzüge", "4", "RKZ", "WKZ", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6", "gym"],
        ["Kniebeugen", "4", "RKB", "WKB", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6", "gym"],
        ["Bizeps KH", "4", "RBZ", "WBZ", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6", "gym"],
        ["Trizeps Seilzug", "4", "RTZ", "WTZ", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6", "gym"],
        ["Seitenheben KH", "4", "RSH", "WSH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6", "gym"]]
    db.addManyEntries(dbName, "training_routine", training)

    trainingAlternatives = [
            [1, "1", "Bankdrücken LH", "Bankdrücken LH", "4", "RBDA", "WBDA", "BDA1", "BDA2", "BDA3", "BDA4", "BDA5", "BDA6", "gym"],
            [5, "2", "TZ Dips", "Trizeps Dips", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6", "gym"],
            [6, "3", "SH Maschine", "Seitenheben Maschine", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6", "gym"],
        ]
    db.addManyEntries(dbName, "training_alternatives", trainingAlternatives)

    trainingNotes = [
            [2, "a", "note 1", "test training note 1"],
            [4, "b", "note 2", "test training note 2"]]
    db.addManyEntries(dbName, "training_notes", trainingNotes)



