# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:53:18 2020

@author: Julian
"""

import sqlite3 as lite
import os, os.path

class database():
    """
    database obects  provide an easy api for working with sqlite3 databases
    and tables. one can create and modify tables. it´s possible to
    create more than one database, by specifying a new database with one
    database-object either by specifying a new path via 'setPath' or by
    invoking the creataDatabase-method with a new database name. the data in a
    table can be retrieved via the data-method (this method fetches all
    avaliable data in a table). to add an new row or an bulk of rows to a table
    one can simply use the method addEntry or addManyEntries respectively. in
    this sense one can use deleteEntry or deleteManyEntries/deleteAllEntries
    do delete one row ora bulk of rows/all rows.

    Properties
    ----------
    - extension : str
        the extension specifies the file-type the database will be
    - path : str
        a path to the target directory, where the database will be stored

    Public Methods
    --------------
    - addEntry : databaseName, tableName, insert
        add a single entry 'insert' to 'tableName' in 'databaseName'

    - addManyEntries : databaseName, tableName, insert
        add a bulk of entries in 'insert' to 'tableName' in 'databaseName'

    - closeConnection : connectionObject
        close a sqlite3.connection object specified by 'connectionObject'

    - createTable : databaseName, tableName, columnNames
        create a table 'tableName' in 'databaseName' with columns specified
        in 'columnNames'

    - deleteAllEntries : databaseName, tableName
        delete all rows in 'tableName' in 'databaseName'

    - deleteManyEntries : databaseName, tableName, row_id_list
        delete only certain rows specified by 'row_id_list' from
        'tableName' in 'databaseName'

    - data : databaseName, tableName
        get all data from 'tableName' in 'databaseName'

    - establishConnection : databaseName
        establish a connection to 'databaseName'

    - extension : None
        getter for the 'extension' property

    - path : None
        getter for the 'path' property

    - setExtension : extension
        setter for the 'extension' property

    - setPath : path
        setter for the 'path' property

    Protected Methods
    -----------------
    __init__ : path = None, extension = ".db"
        constructor of a database-Objet

    __checkPath :  None
        checks input for the property: path. if 'path' remains none, new
        databases are going to be created in the current working directory

    Exmple Usage
    ------------
    db = database(path)

    dbName = "test_database_2"

    columnNames = (
                    ("exercise", "TEXT"),

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

    db.createTable(dbName, "training_routine", columnNames)

    training = [
        ["Bankdrücken KH", "4", "RBD", "WBD", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6", "gym"],

        ["Klimmzüge", "4", "RKZ", "WKZ", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6", "gym"],

        ["Kniebeugen", "4", "RKB", "WKB", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6", "gym"],

        ["Bizeps KH", "4", "RBZ", "WBZ", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6", "gym"],

        ["Trizeps Seilzug", "4", "RTZ", "WTZ", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6", "gym"],

        ["Seitenheben KH", "4", "RSH", "WSH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6", "gym"]
    ]

    db.addManyEntries(dbName, "training_routine", training)
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



    def addEntry(self, databaseName, tableName, insert):
        """
        add a single entry 'insert' to the table named 'tableName' in the database
        'databaseName'.

        Parameters
        ----------
        databaseName : str
            specify the database.
        tableName : str
            specify the table, to wich insert should be added.
        insert : list
            list of values added to the talbe 'tableName'.

        Returns
        -------
        None.

        """

        # establish connection
        con = self.establishConnection(databaseName)

        # do work
        with con:
            c = con.cursor()
            values = '?, ' * len(insert)
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = tableName, values = values)
            c.execute(sql_command, insert)

        # close connection
        self.closeConnection(con)

    def addManyEntries(self, databaseName, tableName, insert):
        """
        add a bulk of rows specified by 'insert' to the table 'tableName' in
        database 'databaseName'

        Parameters
        ----------
        databaseName : str
            specify the database.
        tableName : str
            specify the table, to wich 'insert' should be added.
        insert : list
            list of values added to table 'tableName'. The values have to be
            oreded like this:
                [
                    [value11, value12, ..., value1N],
                    [value21, value22, ..., value2N],
                        .       .               .
                        .       .               .
                        .       .               .
                    [valueN1, valueN2, ..., valueNN]

                ]

        Returns
        -------
        None.

        """

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            values = '?, ' * len(insert[0])
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = tableName, values = values)
            c.executemany(sql_command, insert)

        # close connection
        self.closeConnection(con)

    def closeConnection(self, connectionObject):
        """
        close a connection specified by 'connectionObject'

        Parameters
        ----------
        connectionObject : sqlite3.Connection
            Connection-Object returnded by sqlite3.conntect().

        Returns
        -------
        None.

        """
        connectionObject.close()

    def createDatabase(self, databaseName):
        """
        generates a database called 'databaseName'

        Parameters
        ----------
        databaseName : str
            specify a database to create. if only a name has been pared, the
            database will be created in the current working directory. one can
            also specify 'databaseName' as a path to a certain  directory were
            the database will be created instead

        Returns
        -------
        None.

        """
        con = self.establishConnection(databaseName)
        self.closeConnection(con)

    def createTable(self, databaseName, tableName, columnNames):
        """
        create a table 'tableName' in the database 'databaseName'. the names of
        the columns are specified by 'columnNames'

        Parameters
        ----------
        databaseName : str
            specify the database. if 'databaseName' does not exists, the database
            will be created.
        tableName : str
            specify the table, to wich 'insert' should be added.
        columnNames : tuple
            a tuple of names, specifying the name and type of each column.
            the tuple has to look like the following:

                (
                    ("name1", "type1"),
                    ("name2", "type2"),
                    ("nameN", "typeN")
                )

        the types specified by "type1" to "typeN" have to be sqlite3 conform
        types

        Returns
        -------
        None.

        """
        con = self.establishConnection(databaseName)
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
        self.closeConnection(con)

    def deleteAllEntries(self, databaseName, tableName):
        """
        delete all Entries in the table given by 'tableName' in the database
        called 'databasename'

        Parameters
        ----------
        databaseName : str
            specify the database. if the 'databaseName' refers to a non existing
            database, on OperationalError will be raised
        tableName : str
            specify the tabel, of which the entries will be deleted. if the
            table doesn´t exist, an OperationalError will be raised.

        Returns
        -------
        None.

        """

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name}".format(name = tableName)
            c.execute(sql_command)

        # close connection
        self.closeConnection(con)

    def deleteEntry(self, databaseName, tableName, row_id):
        """
        delete only on line refered by 'row_id' from a table refered by 'tableName'
        in the database called 'databaseName'.

        Parameters
        ----------
        databaseName : str
            specify the database. if 'databaseName' does not exist, an OperationalError
            will be raised
        tableName : str
            specify the table were a certain row will be deleted. if 'tableName'
            does not exist, an OperationalError will be raised
        row_id : int
            specify the row which to delete from the table.

        Returns
        -------
        None.

        """

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                name = tableName, row_id = row_id)
            c.execute(sql_command)

        # close connection
        self.closeConnection(con)

    def deleteManyEntries(self, databaseName, tableName, row_id_list):
        """
        delete a bulk of entries from table 'tableName' in the database
        'databaseName'. 'row_id_list' specifies which rows to delete.

        Parameters
        ----------
        databaseName : str
            specify the database.
        tableName : TYPE
            specify the table form which to delete.
        row_id_list : list
            list of integers defining the rows which to delete.

        Returns
        -------
        None.

        """

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            for idx in row_id_list:
                sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                    name = tableName, row_id = idx)
                c.execute(sql_command)

        # close connection
        self.closeConnection(con)

    def data(self, databaseName, tableName):
        """
        get all data from a table refered by 'tableName' in the database
        refered by 'databaseName'

        Parameters
        ----------
        databaseName : str
            specify the database. if database 'databaseName' does not exist, an
            OperationalError will be raisesd.
        tableName : str
            specify the table from which to fetch data. if table 'tableName'
            does not exist, an OperationalError will be raised.

        Returns
        -------
        data : list
            a nested list, containing  all rows of a table.

        """

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "SELECT * FROM {name}".format(name = tableName)
            c.execute(sql_command)
            data = c.fetchall()

        # close connection
        self.closeConnection(con)

        return data

    def establishConnection(self, databaseName):
        """
        establish a connection to the database 'databaseName'

        Parameters
        ----------
        databaseName : str
            specify the database to connect to.

        Returns
        -------
        sqlite3.Connection Object
            Connection Ojbect describing the connection to a specific database.

        """
        databaseName = databaseName + self.__extension
        database = os.path.join(self.__path, databaseName)
        return lite.connect(database)


    def extension(self):
        """
        extesnion for the database to create a db-file. default is .db

        Returns
        -------
        str
            returns the current extension for all new databases created by
            a Database.database-Object.

        """
        return self.__extension

    def path(self):
        """
        path specifies the directory where new databases are going to be stored

        Returns
        -------
        str
            path to a directory.

        """
        return self.__path

    def setExtension(self, extension):
        """
        set a new value for the property 'extension'

        Parameters
        ----------
        extension : str
            new extensions must have the form ".extension" and must specify a
            valid file-type.

        Returns
        -------
        None.

        """
        self.__extension = extension

    def setPath(self, path):
        npath = os.path.normpath(path)
        self.__path = npath

if __name__ == '__main__':

    # create database
    path = r"C:\Users\Julian\Documents\Python\Projekte\Aphrodite\examples\Qt_ModelView\database"
    db = database(path)
    dbName = "test_database_2"

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
    db.createTable(dbName, "training_routine", columnNames)

    columnNames = (("exerciseID", "INT"),
                   ("label", "TEXT"),
                   ("short", "TEXT"),
                   ("alternative", "TEXT"),
                   ("sets", "TEXT"),
                   ("Repetitions", "TEXT"),
                   ("warm_up", "TEXT"),
                   ("week_1", "TEXT"),
                   ("week_2", "TEXT"),
                   ("week_3", "TEXT"),
                   ("week_4", "TEXT"),
                   ("week_5", "TEXT"),
                   ("week_6", "TEXT"),
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



