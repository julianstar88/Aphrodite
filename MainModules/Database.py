# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:53:18 2020

@author: Julian
"""

import sqlite3 as lite
import pathlib2

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
    - path : str
        a path to the target directory, where the database will be stored
        default: None

    - extension : str
        the extension specifies the file-type the database will be
        default: ".db"

    Public Methods
    --------------
    - addEntry : tableName, insert, databaseName = None
        add a single entry 'insert' to 'tableName' in 'databaseName'

    - addManyEntries : tableName, insert, databaseName = None
        add a bulk of entries in 'insert' to 'tableName' in 'databaseName'

    - closeConnection : connectionObject
        close a sqlite3.connection object specified by 'connectionObject'

    - createDatabase: databaseName = None
        create an empty Database 'databaseName'

    - createTable : tableName, columnNames, databaseName = None
        create a table 'tableName' in 'databaseName' with columns specified
        in 'columnNames'

    - deleteAllEntries : tableName, databaseName = None
        delete all rows in 'tableName' in 'databaseName'

    - deleteEntries : tableName, row_id_list, databaseName = None
        delete only certain rows specified by 'row_id_list' from
        'tableName' in 'databaseName'

    - data : tableName, databaseName = None
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
    1. create a database object

        >>> db = database(path)

    2. create a table

        >>> dbName = "test_database_2"
        >>> columnNames = (
        >>>                ("exercise", "TEXT"),
        >>>                ("sets", "TEXT"),
        >>>                ("repetitions", "TEXT"),
        >>>                ("warm_up", "TEXT"),
        >>>                ("week_1", "TEXT"),
        >>>                ("week_2", "TEXT"),
        >>>                ("week_3", "TEXT"),
        >>>                ("week_4", "TEXT"),
        >>>                ("week_5", "TEXT"),
        >>>                ("week_6", "TEXT"),
        >>>                ("mode", "TEXT"),
        >>>     )
        >>> db.createTable(
        >>>     dbName, "training_routine", columnNames
        >>>     )

    3. add Entries to the table

        >>> training = [
        >>>         ["Bankdrücken KH", "4", "RBD", "WBD", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6", "gym"],
        >>>         ["Klimmzüge", "4", "RKZ", "WKZ", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6", "gym"],
        >>>         ["Kniebeugen", "4", "RKB", "WKB", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6", "gym"],
        >>>         ["Bizeps KH", "4", "RBZ", "WBZ", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6", "gym"],
        >>>         ["Trizeps Seilzug", "4", "RTZ", "WTZ", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6", "gym"],
        >>>         ["Seitenheben KH", "4", "RSH", "WSH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6", "gym"]
        >>>     ]
        >>> db.addManyEntries(
        >>>         dbName, "training_routine", training
        >>>     )

    """

    allowedExtensions = (".db")

    def __init__(self, path = None, extension = ".db"):
        self.__path = None
        self.__databaseName = None
        self.__tables = None
        self.__extension = None

        if self.extension() is None:
            self.setExtension(extension)

        if path is not None:
            self.setPath(path)

        self.__checkPath()

    def __checkPath(self):
        if self.path() is None:
            self.setPath(pathlib2.Path().cwd())

    def addEntry(self, tableName, insert, databaseName = None):
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

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "Databse.addEntry: before adding many etries to a database, set a valid databaseName"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'tableName' of 'addEntry' in 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        if self.tables() is None:
            raise TypeError(
                    "Database.addEntry: there are no tables in database <{name}>".format(
                            name = self.databaseName()
                        )
                )

        if not tableName in self.tables():
            raise ValueError(
                    "input <{input_name}> for 'tableName' of 'addEntry' in 'Database' is not one of {tables}".format(
                            input_name = str(tableName),
                            tables = str(self.tables)
                        )
                )

        path = self.path() / (self.databaseName() + self.extension())
        if not path.is_file():
            raise ValueError(
                    "Database.addEntry: can not add entry to database. database <{name}> does not exist".format(
                            name = self.databaseName()
                        )
                )

        # establish connection
        con = self.establishConnection(self.databaseName())

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

    def addManyEntries(self, tableName, insert, databaseName = None):
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

            >>>    [
            >>>        [value11, value12, ..., value1N],
            >>>        [value21, value22, ..., value2N],
            >>>            .       .               .
            >>>            .       .               .
            >>>            .       .               .
            >>>        [valueN1, valueN2, ..., valueNN]
            >>>    ]

        Returns
        -------
        None.

        """

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "Databse.addManyEntries: before adding many etries to a database, set a valid databaseName"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'tableName' of 'addManyEntries' in 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        if self.tables() is None:
            raise TypeError(
                    "Database.addManyEntries: there are no tables in database"
                )

        if not tableName in self.tables():
            raise ValueError(
                    "input <{input_name}> for 'tableName' of 'addManyEntries' in 'Database' is not one of {tables}".format(
                            input_name = str(tableName),
                            tables = str(self.tables)
                        )
                )

        path = self.path() / (self.databaseName() + self.extension())
        if not path.is_file():
            raise ValueError(
                    "can not add many entries to database. database <{name}> does not exist".format(
                            name = self.databaseName()
                        )
                )

        # establish connection
        con = self.establishConnection(self.databaseName())
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
        if not isinstance(connectionObject, lite.Connection):
            raise TypeError(
                    "input <{input_name}> for 'closeConnection' of 'Database' does not match {type_name}".format(
                            input_name = str(connectionObject),
                            type_name = lite.Connection
                        )
                )

        connectionObject.close()

    def createDatabase(self, databaseName = None):
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

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        con = self.establishConnection(self.databaseName())
        self.closeConnection(con)

    def createTable(self, tableName, columnNames, databaseName = None):
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

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "before creating a table, set a valid databaseName"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'createTable' of 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        con = self.establishConnection(self.databaseName())
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
        self.setTables()

    def databaseName(self):
        """
        Name of the db-file, which serves as data source.

        Returns
        -------
        str

        """
        return self.__databaseName

    def deleteAllEntries(self, tableName, databaseName = None):
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

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "Databse.deleteAllEntries: before adding many etries to a database, set a valid databaseName"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'tableName' of 'deleteAllEntries' in 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        if self.tables() is None:
            raise TypeError(
                    "Database.deleteAllEntries: there are no tables in database"
                )

        if not tableName in self.tables():
            raise ValueError(
                    "input <{input_name}> for 'tableName' of 'deleteAllEntries' in 'Database' is not one of {tables}".format(
                            input_name = str(tableName),
                            tables = str(self.tables)
                        )
                )

        path = self.path() / (self.databaseName() + self.extension())
        if not path.is_file():
            raise ValueError(
                    "Database.deleteAllEntries: database <{name}> does not exist".format(
                            name = self.databaseName()
                        )
                )

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "DELETE FROM {name}".format(name = tableName)
            c.execute(sql_command)

        # close connection
        self.closeConnection(con)

    def deleteEntries(self, tableName, row_id_list, databaseName = None):
        """
        delete a bulk of entries from table 'tableName' in the database
        'databaseName'. 'row_id_list' specifies which rows to delete.

        Parameters
        ----------
        databaseName : str
            specify the database.
        tableName : TYPE
            specify the table form which to delete.
        row_id_list : list or int
            list of integers/ single integer, defining the rows which to delete.

        Returns
        -------
        None.

        """

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "Databse.deleteEntries: before deleting many etries to a database, set a valid databaseName"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'tableName' of 'deleteEntries' in 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        if self.tables() is None:
            raise TypeError(
                    "Database.delteEntries: there are no tables in database"
                )

        if not tableName in self.tables():
            raise ValueError(
                    "input <{input_name}> for 'tableName' of 'deleteEntries' in 'Database' is not one of {tables}".format(
                            input_name = str(tableName),
                            tables = str(self.tables)
                        )
                )

        path = self.path() / (self.databaseName() + self.extension())
        if not path.is_file():
            raise ValueError(
                    "Database.deleteEntries: database <{name}> does not exist".format(
                            name = self.databaseName()
                        )
                )

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            for idx in row_id_list:
                sql_command = "DELETE FROM {name} WHERE rowid = {row_id}".format(
                    name = tableName, row_id = idx)
                c.execute(sql_command)

        # close connection
        self.closeConnection(con)

    def data(self, tableName, databaseName = None):
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

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            raise TypeError(
                    "before retrieving data from a databse, set a valid database"
                )

        if not isinstance(tableName, str):
            raise TypeError(
                    "input <{input_name}> for 'tableName' of 'data' in 'Database' does not match {type_name}".format(
                            input_name = str(tableName),
                            type_name = str
                        )
                )

        if self.tables() is None:
            raise TypeError(
                    "Database.data: there are no tables in database"
                )

        if not tableName in self.tables():
            raise ValueError(
                    "input <{input_name}> for 'tableName' of 'data' in 'Database' is not one of {tables}".format(
                            input_name = str(tableName),
                            tables = str(self.tables)
                        )
                )

        path = self.path() / (self.databaseName() + self.extension())
        if not path.is_file():
            raise ValueError(
                    "Database.data: database <{name}> does not exist".format(
                            name = self.databaseName()
                        )
                )

        # establish connection
        con = self.establishConnection(databaseName)
        with con:
            c = con.cursor()
            sql_command = "SELECT * FROM {name}".format(name = tableName)
            c.execute(sql_command)
            data = c.fetchall()

        # close connection
        self.closeConnection(con)

        # chagne datatype to list
        data = [list(row) for row in data]

        return data

    def establishConnection(self, databaseName = None):
        """
        establish a connection to the database 'databaseName'

        Parameters
        ----------
        databaseName : str
            specify the database to connect to. if databaseName is none, the value
            hold by the databaseName-property will be taken. default is None

        Returns
        -------
        sqlite3.Connection Object
            Connection Ojbect describing the connection to a specific database.

        False
            if one of the following property-types holds None:
                - path()
                - databaseName()
                - extension()

        """

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.databaseName() is None:
            return False

        if self.path() is None:
            return False

        if self.extension() is None:
            return False

        database = self.path() / (self.databaseName() + self.extension())
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
        str or path-like object
            path to a directory.

        """
        return self.__path

    def setDatabaseName(self, databaseName):
        """
        set the name of the db-file, which serves as data-source. if the name
        has a pathlib2.Path().stem and a pathlib2.Path().suffix, the
        'extension' property will be set accordingly, if the suffix is in
        'allowedExtensions'

        Parameters
        ----------
        databaseName : str
            name of the db-file.

        Raises
        ------
        TypeError
            will be raised, if 'databaseName' is not str-type.
        ValueError
            if a pathlib2.Path().suffix exists, and is not in 'allowedExtensions'.

        Returns
        -------
        None.

        """

        if not isinstance(databaseName, str):
            raise TypeError(
                    "input <{input_name}> for 'setDatabaseName' of 'Database' does not match {type_name}".format(
                            input_name = str(databaseName),
                            type_name = str
                        )
                )

        # if len(name.suffix) != 0:
        #     raise ValueError(
        #             "only databaseNames without file-extensions are allowed"
        #         )

        name = pathlib2.Path(databaseName)

        if len(name.suffix) != 0:
            self.__databaseName = name.stem
            self.setExtension(name.suffix)
        else:
            self.__databaseName = databaseName

        self.setTables()

    def setExtension(self, extension):
        """
        set a new value for the property 'extension'

        Parameters
        ----------
        extension : str
            new extensions must have the form ".extension" and must specify a
            valid file-type.

            Default: ".db"

        Returns
        -------
        None.
        """
        if not isinstance(extension, str):
            raise TypeError(
                    "expected {expected_type_name} for 'setExtension' of 'Database', not '{input_type_name}'".format(
                            expected_type_name = type("123"),
                            input_type_name = type(extension)
                        )
                )

        if len(extension) == 0:
            raise ValueError(
                    "empty strings for 'setExtension' of 'Database' are not allowed"
                )

        if extension not in type(self).allowedExtensions:
            raise ValueError(
                    "input <{input_name}> is not allowed. allowed extensions: <{extensions}>".format(
                            input_name = str(extension),
                            extensions = str(type(self).allowedExtensions)
                        )
                )

        self.__extension = extension

    def setPath(self, path):
        """
        set a new path for the property 'path'. the path should point to the
        directory where created database should be stored. if 'path' points to
        a file, 'path' will be set to the parent-directory and the values for
        'databaseName' and 'extension' will be set automatically

        Parameters
        ----------
        path : str, bytes or os.PathLike
            path to a directory.
            Default: None

        Returns
        -------
        None.

        """
        if not isinstance(path, str) and not isinstance(path, pathlib2.Path):
            raise ValueError(
                    "input <{input_name}> for argument 'path' of 'setPath' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = str,
                            type_name_2 = pathlib2.Path()
                        )
                )
        pathObj = pathlib2.Path(path)

        if pathObj.is_file():
            path = pathObj.parent
            name = pathObj.stem
            extension = pathObj.suffix
            self.__path = path
            self.setDatabaseName(name)
            self.setExtension(extension)
            self.setTables()

        if pathObj.is_dir():
            self.__path = pathObj

    def setTables(self, databaseName = None):

        if databaseName is not None:
            self.setDatabaseName(databaseName)

        if self.path() is None:
            raise TypeError(
                    "Database.setTables: before retrieveing the tables in a database, set a valid path"
                )

        if self.databaseName() is None:
            raise TypeError(
                    "Database.setTables: before retrieveing the tables in a database, set a valid databaseName"
                )

        if self.extension() is None:
            raise TypeError(
                    "Database.setTables: before retrieving the tables in a database, set a valid extension"
                )

        path = self.path() / (self.databaseName() + self.extension())

        if not path.is_file():
            return

        con = self.establishConnection()
        if con:
            with con:
                c = con.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                data = c.fetchall()
            self.closeConnection(con)
        else:
            data = []

        self.__tables = [element[0] for element in data]

    def tables(self):
        return self.__tables

if __name__ == '__main__':

    # create database
    path = pathlib2.Path("C:/Users/Julian/Documents/Python/Projekte/Aphrodite/examples/Qt_ModelView/database")
    dbName = "test_database_2"
    db = database()
    db.setPath(path)
    db.setDatabaseName(dbName)

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
    db.createTable("training_routine", columnNames)

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
    db.createTable("training_alternatives", columnNames)


    columnNames = (("excerciseID", "INT"),
                   ("label", "TEXT"),
                   ("short", "TEXT"),
                   ("note", "TEXT"))
    db.createTable("training_notes", columnNames)

    columnNames = (
            ("username", "TXT"),
            ("startDate", "TXT"),
            ("trainingMode", "TXT")
        )
    db.createTable("general_information", columnNames)


    training = [
        ["Bankdrücken KH", "4", "RBD", "WBD", "1.2", "1.4", "1.45", "1.5", "1.6", "1.67", "gym"],
        ["Klimmzüge", "4", "RKZ", "WKZ", "0.6", "0.67 ", "0.8", "0.89", "0.9", "1 ", "gym"],
        ["Kniebeugen", "4", "RKB", "WKB", "2.1", "2.2", "2.35", "2.6", "2.66", "2.67", "gym"],
        ["Bizeps KH", "4", "RBZ", "WBZ", "1.5", "1.45", "1.56", "1.6", "1.67", "1.8", "gym"],
        ["Trizeps Seilzug", "4", "RTZ", "WTZ", "1.21", "1.34", "1.36", "1.38", "1.7", "1.8 ", "gym"],
        ["Seitenheben KH", "4", "RSH", "WSH", "0.2", "0.21", "0.25", "0.5", "0.56", "0.8", "gym"]]
    db.addManyEntries("training_routine", training)

    trainingAlternatives = [
            [1, "1", "Bankdrücken LH", "Bankdrücken LH", "4", "RBDA", "WBDA", "1.1", "1.12", "1.2", "1.3", "1.6", "1.65", "gym"],
            [5, "2", "TZ Dips", "Trizeps Dips", "4", "RSHA", "WSHA", "1.17", "1.18", "1.19", "2.1", "2.5", "2.6", "gym"],
            [6, "3", "SH Maschine", "Seitenheben Maschine", "4", "RSHA", "WSHA", "1.5", "1.55", "1.54", "1.56", "1.7", "2", "gym"],
        ]
    db.addManyEntries("training_alternatives", trainingAlternatives)

    trainingNotes = [
            [2, "a", "note 1", "test training note 1"],
            [4, "b", "note 2", "test training note 2"]]
    db.addManyEntries("training_notes", trainingNotes)

    generalInformation = ["Julian", "28.05.2020", "Mittleres Krafttraining"]
    db.addEntry("general_information", generalInformation)


