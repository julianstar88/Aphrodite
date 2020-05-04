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
        self.database = pathlib2.Path("examples/Qt_ModelView/database/test_database.db")
        self.parentDir = pathlib2.Path().cwd().parent
        self.app = QtWidgets.QApplication(sys.argv)
        self.evaluator = GraphicalEvaluator()
        self.evaluator.setDatabase(str(self.parentDir / self.database))

    def test_initiateQWidgets(self):
        self.evaluator.initiateQWidgets()
        self.assertTrue(
                isinstance(self.evaluator.mainWidget(), QtWidgets.QTabWidget)
            )

    def test_connectEvaluator(self):
        self.evaluator.connectEvaluator(QtWidgets.QWidget())
        self.assertTrue(
                isinstance(self.evaluator.parentWidget(), QtWidgets.QWidget)
            )

    def test_createTabs(self):
        self.evaluator.initiateQWidgets()
        self.evaluator.connectEvaluator(QtWidgets.QWidget())
        self.evaluator.createTabs(self.evaluator.dataFromDatabase())

        data = self.evaluator.dataFromDatabase()
        self.assertEqual(
                self.evaluator.mainWidget().count(), len(data)
            )

        exercises = [line[0] for line in data]
        for i, val in enumerate(exercises):
            with self.subTest(val = val):
                self.assertEqual(
                        self.evaluator.mainWidget().tabText(i), val
                    )

    def test_plotData(self):
        self.evaluator.initiateQWidgets()
        self.evaluator.connectEvaluator(QtWidgets.QWidget())
        self.evaluator.createTabs(self.evaluator.dataFromDatabase())

    def tearDown(self):
        if self.app:
            self.app.quit()

if __name__ == "__main__":
    unittest.main()