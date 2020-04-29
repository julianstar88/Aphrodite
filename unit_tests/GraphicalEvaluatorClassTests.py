# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:02:17 2020

@author: Julian
"""
import unittest
import pathlib2
import os
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

    def test_mainWidget_setter(self):
        self.app = QtWidgets.QApplication([])
        widget = QtWidgets.QWidget()

        self.evaluator.setMainWidget(widget)
        self.assertEqual(
                self.evaluator.mainWidget(), widget
            )

        for val in self.raiseTypeErrors:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError, self.evaluator.setMainWidget, val
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

if __name__ == "__main__":
    unittest.main()