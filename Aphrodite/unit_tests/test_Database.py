# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:29:27 2020

@author: Julian
"""
import unittest
import pathlib2
import sqlite3 as lite
import numpy as np
import MainModules.Database as db

class DatabaseProperties(unittest.TestCase):

    def setUp(self):
        self.currentDir = pathlib2.Path().cwd()
        self.databaseName = "temp_test_database"
        self.databaseFile = self.currentDir / (self.databaseName + ".db")
        self.database = db.database()

    def test_path_getter(self):
        self.assertEqual(
                self.database.path(), pathlib2.Path().cwd()
            )

    def test_extension_getter(self):
        self.assertEqual(
                self.database.extension(), ".db"

            )

    def test_databaseName_getter(self):
        self.assertEqual(
                self.database.databaseName(), None
            )

    def test_tables_getter(self):
        self.assertEqual(
                self.database.tables(), None
            )

    def test_path_setter(self):
        self.database.setPath(self.currentDir.parent)
        self.assertEqual(
                self.database.path(), self.currentDir.parent
            )

    def test_extension_setter(self):
        testValues = [".py", ".txt", ".exe"]

        self.database.setExtension(".db")
        self.assertEqual(
                self.database.extension(), ".db"
            )

        for val in testValues:
            with self.subTest(val = val):
                self.assertRaises(
                        ValueError, self.database.setExtension, val
                    )


    def test_databaseName_setter(self):
        self.database.setDatabaseName(self.databaseName)
        self.assertEqual(
                self.database.databaseName(), self.databaseName
            )

        testName = "test"
        testEx = ".db"
        name = testName + testEx
        self.database.setDatabaseName(name)
        self.assertEqual(
                self.database.databaseName(), testName
            )
        self.assertEqual(
                self.database.extension(), testEx
            )

        testValues = [123, 123.123, (), []]
        for val in testValues:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.database.setDatabaseName, val
                    )

        failNames = ["test.txt", "test.test"]
        for val in failNames:
            with self.subTest(val = val):
                self.assertRaises(
                        ValueError, self.database.setDatabaseName, val
                    )

    def test_tables_setter(self):
        file = pathlib2.Path("test_files/test_database_2.db")

        # TODO this is obsolete, one can work with relative paths instead of
        # absolute ones
        # parentDir = pathlib2.Path().cwd().parent
        # path = parentDir / file

        # the setter will be invoked implicit by using the setPath method
        # by instantiating db.database(path)
        database = db.database(file)

        con = lite.connect(file)
        with con:
            c = con.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            data = c.fetchall()
        con.close()
        tables = [element[0] for element in data]

        self.assertEqual(
                database.tables(), tables
            )

    def tearDown(self):
        try:
            self.databaseFile.unlink()
        except FileNotFoundError: # self.databaseFile does not exist
            pass

class DatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.currentDir = pathlib2.Path().cwd()
        self.databaseName = "temp_test_database"
        self.tableName = "test_table"
        self.database = db.database(self.currentDir)
        self.databaseFile = self.currentDir / (self.databaseName + self.database.extension())

    def test_data(self):
        # TODO this is obsolete. one can work with relative paths instead of
        # createing absolute ones
        #
        # file = pathlib2.Path("files/test_files/test_database_2.db")
        # parentDir = pathlib2.Path().cwd().parent
        # path = parentDir / file
        # database = db.database(path)
        file = pathlib2.Path("test_files/test_database_2.db")
        database = db.database(file)
        tableName = "training_routine"
        data = database.data(tableName)
        array = np.array(data)

        self.assertEqual(
                len(array.shape), 2
            )

        self.assertNotEqual(
                array.size, 0
            )

    def test_createDatabase(self):
        self.database.createDatabase(self.databaseName)
        self.assertTrue(
                self.databaseFile.is_file()
            )

    def test_createTable(self):
        colNames = (
                ("one", "TEXT"),
                ("two", "TEXT"),
                ("three", "TEXT")
            )
        self.database.createTable(self.tableName, colNames, self.databaseName)

        con = self.database.establishConnection(self.databaseName)
        with con:
            c = con.cursor()
            c.execute("SELECT * FROM {}".format(self.tableName))
            colList = [description[0] for description in c.description]
        self.database.closeConnection(con)

        for i, val in enumerate(colList):
            with self.subTest(val = val):
                self.assertEqual(
                        val, colNames[i][0]
                    )

    def test_addEntry(self):
        colNames = (
                ("one", "INT"),
                ("two", "INT"),
                ("three", "INT")
            )
        insert = [1, 2, 3]
        self.database.createTable(self.tableName, colNames, self.databaseName)
        self.database.addEntry(self.tableName, insert)
        data = self.database.data(self.tableName)
        array = np.array(data)

        self.assertEqual(
                len(array.shape), 2
            )

        self.assertNotEqual(
                array.size, 0
            )

        for n in range(array.shape[0]):
            for m in range(array.shape[1]):
                self.assertEqual(
                        array[n, m], insert[m]
                    )

    def test_addManyEntries(self):
        colNames = (
                ("one", "INT"),
                ("two", "INT"),
                ("three", "INT")
            )
        insert = [[1, 2, 3], [4,5,6], [7,8,9]]
        self.database.createTable(self.tableName, colNames, self.databaseName)
        self.database.addManyEntries(self.tableName, insert)
        data = self.database.data(self.tableName)
        array = np.array(data)

        self.assertEqual(
                len(array.shape), 2
            )

        self.assertNotEqual(
                array.size, 0
            )

        for n in range(array.shape[0]):
            for m in range(array.shape[1]):
                self.assertEqual(
                        array[n, m], insert[n][m]
                    )

    def test_deleteAllEntries(self):
        colNames = (
                ("one", "INT"),
                ("two", "INT"),
                ("three", "INT")
            )
        insert = [[1, 2, 3], [4,5,6], [7,8,9]]
        self.database.createTable(self.tableName, colNames, self.databaseName)
        self.database.addManyEntries(self.tableName, insert)

        self.database.deleteAllEntries(self.tableName)
        data = self.database.data(self.tableName)
        array = np.array(data)

        self.assertEqual(
                array.size, 0
            )

    def test_deleteEntries(self):
        colNames = (
                ("one", "INT"),
                ("two", "INT"),
                ("three", "INT")
            )
        insert = [[1, 2, 3], [4,5,6], [7,8,9], [10,11,12]]
        inputArray = np.array(insert)
        deleteRow = [3]
        deleteRows = [1, 2]
        self.database.createTable(self.tableName, colNames, self.databaseName)
        self.database.addManyEntries(self.tableName, insert)

        self.database.deleteEntries(self.tableName, deleteRow)
        data = self.database.data(self.tableName)
        array = np.array(data)

        self.assertEqual(
                len(array.shape), 2
            )

        self.assertEqual(
                array.shape[0], inputArray.shape[0]-1
            )

        self.assertNotEqual(
                array.size, 0
            )

        self.database.deleteEntries(self.tableName, deleteRows)
        data = self.database.data(self.tableName)
        array = np.array(data)

        self.assertEqual(
                array.shape[0], inputArray.shape[0]-3
            )

        self.assertNotEqual(
                array.size, 0
            )

    def test_deleteTable(self):
        type_error = [1, 123, 123.123, (), [], {}]
        value_error = "failTableName"
        self.database.createDatabase(self.databaseName)
        columnNames = (
                ("test1", "TXT"),
                ("test2", "TXT"),
                ("test3", "TXT")
            )
        self.database.createTable("testTable", columnNames)
        for val in type_error:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.database.deleteTable, val
                    )
        self.assertRaises(
                ValueError, self.database.deleteTable, value_error
            )
        self.database.deleteTable("testTable")
        self.assertEqual(len(self.database.tables()), 0)

    def tearDown(self):
        try:
            self.databaseFile.unlink()
        except FileNotFoundError: # self.databaseFile does not exist
            pass

class ConvenientMethods(unittest.TestCase):

    def setUp(self):
        self.path = pathlib2.Path().cwd()
        self.databaseName = "test_convenient_methods"
        self.database = db.database()
        self.database.setDatabaseName(self.databaseName)
        self.database.setPath(self.path)
        self.database.createDatabase()
        self.file = self.database.path() / (self.database.databaseName() + self.database.extension())

    def test_createRoutineTables(self):
        result = self.database.createRoutineTables()
        self.assertTrue(result)

    def test_setGeneralInformation(self):
        fails = [
                    [1, 1, 1],
                    [123, 123, 123],
                    [123.123, 123.123, 123.123],
                    [(), (), ()],
                    [[], [], []],
                    [{}, {}, {}]
            ]
        self.database.createRoutineTables()

        for val in fails:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.database.setGeneralInformation, val[0], val[1], val[2], debugging = True
                    )

        result = self.database.setGeneralInformation("testUser", "11.11.2020", "testMode")
        self.assertTrue(result)

    def test_addTrainingRoutine(self):
        self.database.createRoutineTables()
        result = self.database.addTrainingRoutine(
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testValue",
                "testMode"
            )
        self.assertTrue(result)

    def test_addTrainingAlternative(self):
        self.database.createRoutineTables()
        result = self.database.addTrainingAlternative(
                1,
                "testAlternativeExercise",
                "testSets",
                "testReps",
                "testWarmUp",
                "testWeek1",
                "testWeek2",
                "testWeek3",
                "testWeek4",
                "testWeek5",
                "testWeek6",
                "testMode",
            )
        self.assertTrue(result)

    def test_addTrainingNote(self):
        self.database.createRoutineTables()
        result = self.database.addTrainingNote(
                1,
                "ThisIsATestNote",
            )
        self.assertTrue(result)

    def test_isValid(self):
        fails = ["", "fail", "fail.db"]

        result = self.database.isValid()
        self.assertTrue(result)

        for val in fails:
            self.database.setDatabaseName(val)
            with self.subTest(val = val):
                result = self.database.isValid()
                self.assertFalse(result)

    def tearDown(self):
        try:
            self.file.unlink()
        except FileNotFoundError: # self.databaseFile does not exist
            pass

if __name__ == "__main__":
    unittest.main()