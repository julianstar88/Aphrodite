# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:02:17 2020

@author: Julian
"""
import unittest
import pathlib2
import os
import sys
import MainModules.Database as db
from PyQt5 import QtWidgets
from MainModules.GraphicalEvaluator import GraphicalEvaluator
from UtilityModules.CustomModel import CustomSqlModel

class GraphicalEvaluatorProperties(unittest.TestCase):

    def setUp(self):
        self.raiseTypeErrors = [
                123,
                123.123,
                [],
                (),
                {},
            ]
        self.raiseValueErrors = [
                "randomParent/randomPath/randomFile",
                ""
            ]
        self.evaluator = GraphicalEvaluator()
        self.app = None
        self.databasePath = None

    def test_database_getter(self):
        self.assertEqual(
                self.evaluator.database(), None
            )

    def test_mainWidget_getter(self):
        self.assertEqual(
                self.evaluator.mainWidget(), None
            )

    def test_model_getter(self):
        self.assertEqual(
                self.evaluator.model(), None
            )

    def test_parentWidget_getter(self):
        self.assertEqual(
                self.evaluator.parentWidget(), None
            )

    def test_database_setter(self):
        databaseParentPath = pathlib2.Path().cwd()
        databaseName = "temp_test_database"
        self.databasePath = databaseParentPath / pathlib2.Path(databaseName + ".db")
        database = db.database(str(databaseParentPath))
        database.createDatabase(databaseName)
        self.evaluator.setDatabase(str(self.databasePath))

        self.assertEqual(
                self.evaluator.database(), str(self.databasePath)
            )

        for val in self.raiseTypeErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.evaluator.setDatabase, val
                    )

        for val in self.raiseValueErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        ValueError, self.evaluator.setDatabase, val
                    )

    def test_model_setter(self):
        model = CustomSqlModel()

        self.evaluator.setModel(model)
        self.assertEqual(
                self.evaluator.model(), model
            )

        for val in self.raiseTypeErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.evaluator.setModel, val
                    )

    def test_parentWidget_setter(self):
        self.app = QtWidgets.QApplication([])
        widget = QtWidgets.QWidget()

        self.evaluator.initiateQWidgets()
        self.evaluator.setParentWidget(widget)
        self.assertEqual(
                self.evaluator.parentWidget(), widget
            )

        for val in self.raiseTypeErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.evaluator.setParentWidget, val
                    )


    def tearDown(self):
        if self.app:
            self.app.quit()
        if self.databasePath:
            os.remove(self.databasePath)

class EvaluatorLayout(unittest.TestCase):

    def setUp(self):
        self.raiseTypeErrors = [
                123,
                123.123,
                {},
            ]
        self.raiseValueErrors = [
                [1,2,3],
                (1,2,3),
            ]

        self.database = pathlib2.Path("test_files/test_database_2.db")
        self.parentDir = pathlib2.Path().cwd().parent
        self.evaluator = GraphicalEvaluator()
        self.evaluator.setDatabase(self.database)

    def test_initiateQWidgets(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        testWidget = QtWidgets.QWidget()
        mainWindow.setCentralWidget(testWidget)
        self.evaluator.initiateQWidgets()
        self.assertTrue(
                isinstance(self.evaluator.mainWidget(), QtWidgets.QTabWidget)
            )
        app.quit()

    def test_connectEvaluator(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        testWidget = QtWidgets.QWidget()
        mainWindow.setCentralWidget(testWidget)
        self.evaluator.connectEvaluator(testWidget)
        self.assertTrue(
                isinstance(self.evaluator.parentWidget(), QtWidgets.QWidget)
            )
        app.quit()

    def test_createTabs(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        testWidget = QtWidgets.QWidget()
        mainWindow.setCentralWidget(testWidget)
        self.evaluator.initiateQWidgets()
        self.evaluator.connectEvaluator(testWidget)
        self.evaluator.createTabs(self.evaluator.dataFromDatabase())

        data = self.evaluator.dataFromDatabase()
        self.assertEqual(
                self.evaluator.mainWidget().count(), len(data)
            )

        for val in self.raiseTypeErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.evaluator.createTabs, val
                    )

        for val in self.raiseValueErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        ValueError, self.evaluator.createTabs, val
                    )

        exercises = [line[0] for line in data]
        for i, val in enumerate(exercises):
            with self.subTest(val = val):
                self.assertEqual(
                        self.evaluator.mainWidget().tabText(i), val
                    )
        app.quit()

if __name__ == "__main__":
    unittest.main()