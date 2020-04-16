# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:37:34 2020

@author: Julian
"""


import unittest
import datetime
from MainModules.Exporter import Exporter

class ExporterBaseTest(unittest.TestCase):

    def setUp(self):
        self.exporter = Exporter()

    def test_instance(self):
        self.assertIsInstance(
                self.exporter, Exporter,
                msg = "Test: <{method}> failed".format(
                        method = "test_instance"
                    )
            )

    def test_name_getter(self):
        self.assertEqual(
                self.exporter.name(), None,
                msg = "Test: <{method}> failed".format(
                        method = "test_name_getter"
                    )
            )

    def test_routineName_getter(self):
        self.assertEqual(
                self.exporter.routineName(), None,
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_getter"
                    )
            )

    def test_trainingPeriode_getter(self):
        self.assertEqual(
                self.exporter.trainingPeriode(), [None, None],
                msg = "Test: <{method} failed>".format(
                        method = "test_trainingPeriode_getter"
                    )
            )

    def test_name_setter(self):
        self.exporter.setName("Test Name")
        self.assertEqual(self.exporter.name(), "Test Name")
        self.assertRaises(
                TypeError, self.exporter.setName, 123,
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setName, 123.123,
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setName, [],
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setName, (),
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setName, {},
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setName, "",
                msg = "Test: <{method}> failed".format(
                        method = "test_name_setter"
                    )
            )

    def test_routineName_setter(self):
        self.exporter.setRoutineName("Test Name")
        self.assertEqual(
                self.exporter.routineName(), "Test Name",
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, 123,
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, 123.123,
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, [],
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, (),
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, {},
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )
        self.assertRaises(
                TypeError, self.exporter.setRoutineName, "",
                msg = "Test: <{method}> failed".format(
                        method = "test_routineName_setter"
                    )
            )

    def test_trainingPeriode_setter(self):
        start = datetime.date(2020, 4, 16)
        end = start + datetime.timedelta(days = 42)
        testValues = ("", 123.124, (), [], {})
        self.exporter.setTrainingPeriode(2020, 4, 16)
        self.assertEqual(
                self.exporter.trainingPeriode(), (start, end),
                msg = "Test: <{method}> failed".format(
                        method = "test_trainingPeriode_setter"
                    )
            )
        for value in testValues:
            self.assertRaises(
                    TypeError, self.exporter.setTrainingPeriode, value, 2, 3,
                    msg = "Test: <{method}> failed".format(
                            method = "test_trainingPeriode_setter"
                        )
                )
        for value in testValues:
            self.assertRaises(
                    TypeError, self.exporter.setTrainingPeriode, 1, value, 3,
                    msg = "Test: <{method}> failed".format(
                            method = "test_trainingPeriode_setter"
                        )
                )
        for value in testValues:
            self.assertRaises(
                    TypeError, self.exporter.setTrainingPeriode, 1, 2, value,
                    msg = "Test: <{method}> failed".format(
                            method = "test_trainingPeriode_setter"
                        )
                )

class ExporterLayoutTest(unittest.TestCase):

    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()
