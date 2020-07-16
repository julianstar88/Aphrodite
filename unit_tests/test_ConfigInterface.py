# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:48:17 2020

@author: Julian
"""

import unittest
import pathlib2

from MainModules import ConfigInterface

class ConfigInterfaceProperties(unittest.TestCase):

    def setUp(self):
        self.configParser = ConfigInterface.ConfigParser()
        self.configFile = pathlib2.Path("test_files/test_config.txt")

    def test_configFileName_getter(self):
        self.assertIsNone(
                self.configParser.configFileName()
            )

    def test_configDir_getter(self):
        self.assertIsNone(
                self.configParser.configDir()
            )

    def test_configFileName_setter(self):
        configFileName = self.configFile.stem
        TypeFail = [123, 123.123, self.configParser]

        self.configParser.setConfigFileName(configFileName)
        self.assertEqual(
                self.configParser.configFileName(), configFileName
            )

        for val in TypeFail:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError,
                        self.configParser.setConfigFileName,
                        val
                    )

    def test_configDir_setter(self):
        configDir = self.configFile.parent
        configFileName = self.configFile.name
        TypeFail = [123, 123.123, self.configParser]
        ValueFail = "random/test/file.txt"

        self.configParser.setConfigDir(configDir)
        self.assertEqual(
                self.configParser.configDir(), configDir
            )
        self.configParser.setConfigDir(str(configDir))
        self.assertEqual(
                self.configParser.configDir(), configDir
            )

        self.configParser.setConfigDir(self.configFile)
        self.assertEqual(
                self.configParser.configDir(), configDir
            )
        self.assertEqual(
                self.configParser.configFileName(), configFileName
            )
        self.configParser.setConfigDir(str(self.configFile))
        self.assertEqual(
                self.configParser.configDir(), configDir
            )
        self.assertEqual(
                self.configParser.configFileName(), configFileName
            )

        self.assertRaises(
                ValueError,
                self.configParser.setConfigDir,
                ValueFail
            )

        for val in TypeFail:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError,
                        self.configParser.setConfigDir,
                        val
                    )

class ConfigInterfaceMethods(unittest.TestCase):

    def setUp(self):
        self.testFile = pathlib2.Path("test_files/test_config.txt")
        self.outputFile = pathlib2.Path("test_files/output.txt")
        self.configParser = ConfigInterface.ConfigParser()

    def test_addAttributes(self):
        TypeFail = [123, 123.123, "123", {}, self.configParser]

        self.configParser.addAttributes(["test"], ["test"])
        self.assertEqual(
                self.configParser.test, "test"
            )

        # test for TypeError for first input argument
        for val in TypeFail:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError,
                        self.configParser.addAttributes,
                        val,["test"]
                    )

        # test for TypeError for second input argument
        for val in TypeFail:
            with self.subTest(val = val):
                self.assertRaises(
                        TypeError,
                        self.configParser.addAttributes,
                        ["test"], val
                    )

    def test_readAttributes(self):
        testKeys = ["test1", "test2", "test3"]
        testValues = ["testValue1", "testValue2", "testValue3"]
        self.configParser.addAttributes(testKeys, testValues)
        result = self.configParser.readAttributes()

        # convert output dict to list for testing
        result = list(result.items())

        # test output for keys in test_config.txt
        for i, val in enumerate(testKeys):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][0], val
                    )

        # test output for values in test_config.txt
        for i, val in enumerate(testValues):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][1], val
                    )

    def test_readConfigFile(self):

        # read test_config.txt seperately from configParser
        # to gather test values
        with open(self.testFile, "r") as file:
            rawLines = file.readlines()
        testValues = list()
        for line in rawLines:
            stripped = line.strip("\n")
            splitted = stripped.split(":")
            testValues.append(splitted)

        # read test_config.txt by configParser.readConfigFile
        self.configParser.readConfigFile(self.testFile)
        result = list(self.configParser.readAttributes().items())

        # test ouput for keys from readConfigFile
        for i, val in enumerate(testValues):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][0], testValues[i][0]
                    )

        # test ouput for values from readConfigFile
        for i, val in enumerate(testValues):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][1], testValues[i][1]
                    )

    def test_writeConfigFile(self):
        testKeys = ["test1", "test2", "test3"]
        testValues = ["testValue1", "testValue2", "testValue3"]

        # generate ouput file
        self.configParser.addAttributes(testKeys, testValues)
        self.configParser.writeConfigFile(
                fileName = self.outputFile.name,
                wdir = self.outputFile.parent
            )

        # test output for self.configParser.writeConfigFile()
        self.configParser.readConfigFile(
                file = self.outputFile
            )
        result = list(self.configParser.readAttributes().items())

        for i, val in enumerate(testKeys):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][0], val
                    )

        for i, val in enumerate(testValues):
            with self.subTest(val = val):
                self.assertEqual(
                        result[i][1], val
                    )

    def tearDown(self):
        try:
            self.outputFile.unlink()
        except FileNotFoundError: # outputFile does not exist
            pass


if __name__ == "__main__":
    unittest.main()
