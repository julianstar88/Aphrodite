# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:53:18 2020

@author: Julian
"""

import sqlite3 as lite

class database():
    """
    Create a SQlite3 database file with the name 'name' and the columns
    'columns'.

    Input parameter:
        -name: name of the generated database-file type: str
        -column_names: name and type of the colums in form of an tupel
            (("name", "type"), ("name", "type"),...)

    Output:
        - A db-file named 'name'
    """
    def __init__(self, databaseName, tableName, columnNames):
        self.__name = databaseName
        # self.__column_names = column_names

        # self.table_name = table_name

        # self.__con = None

        # establish connection to a database or create it if it not exists
        con = self.__establishConnection(databaseName)

        # create table
        with con:

            cur = con.cursor()
            # cur = self.__con.cursor()

            # comment if existing database-files should not be overwritten
            cur.execute("DROP TABLE IF EXISTS {name}".format(name = tableName))
            valueString = ""
            for names in columnNames:
                valueString = valueString + "{} {}, ".format(names[0], names[1])
            valueString = valueString[:-2]
            cur.execute("CREATE TABLE {}({})".format(tableName, valueString))

        # close connection after work is done
        self.__closeConnection(con)

    def createTable(self, tableName, columnNames):
        con = self.__establishConnection(self.__name)
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


    def addEntry(self, tableName, insert):

        # establish connection
        con = self.__establishConnection(self.__name)

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

    def addManyEntries(self, tableName, insert):

        # establish connection
        con = self.__establishConnection(self.__name)
        with con:
            c = con.cursor()
            values = '?, ' * len(insert[0])
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = tableName, values = values)
            c.executemany(sql_command, insert)

        # close connection
        self.__closeConnection(con)

    def deleteEntry(self, tableName, row_id):

        # establish connection
        con = self.__establishConnection(self.__name)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                name = tableName, row_id = row_id)
            c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def deleteManyEntries(self, tableName, row_id_list):

        # establish connection
        con = self.__establishConnection(self.__name)
        with con:
            c = self.__con.cursor()
            for idx in row_id_list:
                sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                    name = tableName, row_id = idx)
                c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def deleteAllEntries(self, tableName):

        # establish connection
        con = self.__establishConnection(self.__name)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name}".format(name = tableName)
            c.execute(sql_command)

        # close connection
        self.__closeConnection(con)

    def getData(self, tableName):

        # establish connection
        con = self.__establishConnection(self.__name)
        with con:
            c = self.__con.cursor()
            sql_command = "SELECT * FROM {name}".format(name = tableName)
            c.execute(sql_command)
            data = c.fetchall()

        # close connection
        self.__closeConnection(con)

        return data

    def __establishConnection(self, databaseName):
        return lite.connect(databaseName)
        # self.__con = lite.connect(databaseName)

    def __closeConnection(self, connectionObject):
        connectionObject.close()
        # self.__con.close()



if __name__ == '__main__':

    # create databases
    # columnNames = ( ("id", "INT"),
    #                 ("Exercise", "TEXT"),
    #                 ("Sets", "TEXT"),
    #                 ("Repetitions", "TEXT"),
    #                 ("Warm_Up", "TEXT"),
    #                 ("Week_1", "TEXT"),
    #                 ("Week_2", "TEXT"),
    #                 ("Week_3", "TEXT"),
    #                 ("Week_4", "TEXT"),
    #                 ("Week_5", "TEXT"),
    #                 ("Week_6", "TEXT"))
    columnNames = ( ("Exercise", "TEXT"),
                    ("Sets", "TEXT"),
                    ("Repetitions", "TEXT"),
                    ("Warm_Up", "TEXT"),
                    ("Week_1", "TEXT"),
                    ("Week_2", "TEXT"),
                    ("Week_3", "TEXT"),
                    ("Week_4", "TEXT"),
                    ("Week_5", "TEXT"),
                    ("Week_6", "TEXT"))

    db = database("test_database.db", "training_routine", columnNames)

    # columnNames = (("id", "INT"),
    #                ("exerciseID", "INT"),
    #                ("label", "TEXT"),
    #                ("short", "TEXT"),
    #                ("alternative", "TEXT"),
    #                ("Sets", "TEXT"),
    #                ("Repetitions", "TEXT"),
    #                ("Warm_Up", "TEXT"),
    #                ("Week_1", "TEXT"),
    #                ("Week_2", "TEXT"),
    #                ("Week_3", "TEXT"),
    #                ("Week_4", "TEXT"),
    #                ("Week_5", "TEXT"),
    #                ("Week_6", "TEXT"))
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
                   ("Week_6", "TEXT"))


    db.createTable("training_alternatives", columnNames)

    # columnNames = (("id", "INT"),
    #                ("excerciseID", "INT"),
    #                ("label", "TEXT"),
    #                ("short", "TEXT"),
    #                ("note", "TEXT"))
    columnNames = (("excerciseID", "INT"),
                   ("label", "TEXT"),
                   ("short", "TEXT"),
                   ("note", "TEXT"))


    db.createTable("training_notes", columnNames)


    # training = [
    #     [1, "Bankdrücken KH", "4", "RBD", "WBD", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6"],
    #     [2, "Klimmzüge", "4", "RKZ", "WKZ", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6"],
    #     [3, "Kniebeugen", "4", "RKB", "WKB", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6"],
    #     [4, "Bizeps KH", "4", "RBZ", "WBZ", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6"],
    #     [5, "Trizeps Seilzug", "4", "RTZ", "WTZ", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6"],
    #     [6, "Seitenheben KH", "4", "RSH", "WSH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6"]]
    training = [
        ["Bankdrücken KH", "4", "RBD", "WBD", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6"],
        ["Klimmzüge", "4", "RKZ", "WKZ", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6"],
        ["Kniebeugen", "4", "RKB", "WKB", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6"],
        ["Bizeps KH", "4", "RBZ", "WBZ", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6"],
        ["Trizeps Seilzug", "4", "RTZ", "WTZ", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6"],
        ["Seitenheben KH", "4", "RSH", "WSH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6"]]

    db.addManyEntries("training_routine", training)

    # trainingAlternatives = [
    #         [1, 1, "1", "Bankdrücken LH", "Bankdrücken LH", "4", "RBDA", "WBDA", "BDA1", "BDA2", "BDA3", "BDA4", "BDA5", "BDA6"],
    #         [2, 5, "2", "TZ Dips", "Trizeps Dips", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6"],
    #         [3, 6, "3", "SH Maschine", "Seitenheben Maschine", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6"],
    #     ]
    trainingAlternatives = [
            [1, "1", "Bankdrücken LH", "Bankdrücken LH", "4", "RBDA", "WBDA", "BDA1", "BDA2", "BDA3", "BDA4", "BDA5", "BDA6"],
            [5, "2", "TZ Dips", "Trizeps Dips", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6"],
            [6, "3", "SH Maschine", "Seitenheben Maschine", "4", "RSHA", "WSHA", "SHA1", "SHA2", "SHA3", "SHA4", "SHA5", "SHA6"],
        ]
    db.addManyEntries("training_alternatives", trainingAlternatives)

    # trainingNotes = [
    #         [1, 2, "a", "note 1", "test training note 1"],
    #         [2, 4, "b", "note 2", "test training note 2"]]
    trainingNotes = [
            [2, "a", "note 1", "test training note 1"],
            [4, "b", "note 2", "test training note 2"]]
    db.addManyEntries("training_notes", trainingNotes)



