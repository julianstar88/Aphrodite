# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:29:27 2020

@author: Julian
"""
import unittest
import pathlib2
import numpy as np
import MainModules.Database as db

class DatabaseProperties(unittest.TestCase):

    def setUp(self):
        self.currentDir = pathlib2.Path().cwd()
        self.databaseName = "temp_test_database"
        self.database = db.database()

    def test_path_getter(self):
        self.assertEqual(
                self.database.path(), str(pathlib2.Path().cwd())
            )

    def test_extension_getter(self):
        self.assertEqual(
                self.database.extension(), ".db"
            )

    def test_path_setter(self):
        self.database.setPath(str(self.currentDir.parent))
        self.assertEqual(
                self.database.path(), str(self.currentDir.parent)
            )

    def test_extension_setter(self):
        self.database.setExtension(".test")
        self.assertEqual(
                self.database.extension(), ".test"
            )

    def tearDown(self):
        pass

class DatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.currentDir = pathlib2.Path().cwd()
        self.databaseName = "temp_test_database"
        self.tableName = "test_table"
        self.database = db.database(str(self.currentDir))
        self.databaseFile = self.currentDir / (self.databaseName + self.database.extension())

    def test_data(self):
        file = pathlib2.Path("files/test_files/test_database_2.db")
        parentDir = pathlib2.Path().cwd().parent / file.parent
        database = db.database(str(parentDir))
        databaseName = file.stem
        tableName = "training_routine"
        data = database.data(databaseName, tableName)
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
        self.database.createTable(self.databaseName, self.tableName, colNames)

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
        self.database.createTable(self.databaseName, self.tableName, colNames)
        self.database.addEntry(self.databaseName, self.tableName, insert)
        data = self.database.data(self.databaseName, self.tableName)
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
        self.database.createTable(self.databaseName, self.tableName, colNames)
        self.database.addManyEntries(self.databaseName, self.tableName, insert)
        data = self.database.data(self.databaseName, self.tableName)
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
        self.database.createTable(self.databaseName, self.tableName, colNames)
        self.database.addManyEntries(self.databaseName, self.tableName, insert)

        self.database.deleteAllEntries(self.databaseName, self.tableName)
        data = self.database.data(self.databaseName, self.tableName)
        array = np.array(data)

        self.assertEqual(
                array.size, 0
            )

    def deleteManyEntries(self):
        colNames = (
                ("one", "INT"),
                ("two", "INT"),
                ("three", "INT")
            )
        insert = [[1, 2, 3], [4,5,6], [7,8,9], [10,11,12]]
        inputArray = np.array(insert)
        deleteRow = 3
        deleteRows = [1, 2]
        self.database.createTable(self.databaseName, self.tableName, colNames)
        self.database.addManyEntries(self.databaseName, self.tableName, insert)

        self.database.deleteManyEntries(self.databaseName, self.tableName, deleteRow)
        data = self.database.data(self.databaseName, self.tableName)
        array = np.array(data)

        self.asserEqual(
                len(array.shape), 2
            )

        self.assertEqual(
                array.shape[0], inputArray[0]-1
            )

        self.assertNotEqual(
                array.size, 0
            )

        self.database.deleteManyEntries(self.databaseName, self.tableName, deleteRows)
        data = self.database.data(self.databaseName, self.tableName)
        array = np.array(data)

        self.assertEqual(
                array.shape[0], inputArray.shape[0]-3
            )

        self.assertNotEqual(
                array.size, 0
            )

    def tearDown(self):
        try:
            self.databaseFile.unlink()
        except FileNotFoundError: # self.databaseFile does not exist
            pass


if __name__ == "__main__":
    unittest.main()