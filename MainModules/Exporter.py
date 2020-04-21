# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:14 2020

@author: Julian
"""
import datetime
import pathlib2
import openpyxl
import UtilityModules.ExporterUtilityModules as exporterUtils


class Exporter():

    def __init__(self,
                 database = None,
                 exportPath = None,
                 name = None,
                 routineName = None,
                 trainingPeriode = [None, None],
                 trainingMode = None,
                 workBook = None):

        self.__database = database
        self.__exportPath = exportPath
        self.__name = name
        self.__routineName = routineName
        self.__trainingPeriode = trainingPeriode
        self.__trainingMode = trainingMode
        self.__workBook = workBook

    def database(self):
        return self.__database

    def exportPath(self):
        return self.__exportPath

    def name(self):
        return self.__name

    def populateRoutine(self):
        pass

    def routineLayout(self, rows = 40):
        workBook = exporterUtils.TamplateLayout(rows)
        return workBook

    def routineName(self):
        return self.__routineName

    def trainingMode(self):
        return self.__trainingMode

    def trainingPeriode(self):
        return self.__trainingPeriode


    def setDatabase(self, databasePath):
        path = pathlib2.Path(databasePath)
        if not type(databasePath) == str:
            raise TypeError(
                    "input {input_value} for argument 'databasePath' does not match {type_name}".format(
                            input_value = path,
                            type_name = type("str")
                        )
                )
        if not path.exists():
            raise ValueError(
                    "Database does not exist"
                )
        if len(databasePath) == 0:
            raise ValueError(
                    "invalid input for argument 'databasePath'"
                )
        self.__database = str(path)

    def setExportPath(self, exportPath):
        path = pathlib2.Path(exportPath)
        if not type(exportPath) == str:
            raise TypeError(
                    "input for argument 'exportPath' does not match {type_name}".format(
                            input_name = path,
                            type_name = type("str")
                        )
                )
        if not path.is_dir():
            raise ValueError(
                    "input for argument 'exportPath' does not refer to an existing directory"
                )
        if len(exportPath) == 0:
            raise ValueError(
                    "invalid input for argument 'exportPath'"
                )
        self.__exportPath = str(path)

    def setName(self, name):
        if not type(name) == str:
            raise TypeError(
                "input argument {name} does not match {type_name}".format(
                        name = name,
                        type_name = type("str")
                    )
                )
        elif len(name) == 0:
            raise ValueError("empty input for the attribute 'name'")
        else:
            self.__name = name

    def setRoutineName(self, routineName):
        if not type(routineName) == str:
            raise TypeError(
                "input argument {name} does not match {type_name}".format(
                        name = routineName,
                        type_name = type("str")
                    )
                )
        elif len(routineName) == 0:
            raise ValueError("empty input for the attribute 'routineName'")
        else:
            self.__routineName = routineName

    def setTrainingMode(self, trainingMode):
        if not type(trainingMode) == str:
            raise TypeError(
                    "input {input_name} for argument 'trainingMode' does not match {type_name}".format(
                            input_name = type(trainingMode),
                            type_name = type("123")
                        )
                )
        if len(trainingMode) == 0:
            raise ValueError(
                    "input for 'trainingMode' is not valid. 'trainingMode' must at least contain one character"
                )
        self.__trainingMode = trainingMode

    def setTrainingPeriode(self, startYear, startMonth, startDay):
        if not type(startYear) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {type_name}""".format(
                            name = startYear,
                            type_name = type(123)
                        )
                )
        if not type(startMonth) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {type_name}""".format(
                            name = startMonth,
                            type_name = type(123)
                        )
                )
        if not type(startDay) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {type_name}""".format(
                            name = startDay,
                            type_name = type(123)
                        )
                )
        startDate = datetime.date(startYear, startMonth, startDay)
        endDate = startDate + datetime.timedelta(days = 42)
        startDateString = startDate.strftime("%d.%m.%Y")
        endDateString = endDate.strftime("%d.%m.%Y")
        self.__trainingPeriode = (startDateString, endDateString)

    def setWorkBook(self, workBook):
        if not type(workBook) == openpyxl.Workbook:
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'openpyxl.Workbook' module"
                )
        self.__workBook = workBook

    def workBook(self):
        return self.__workBook

if __name__ == "__main__":
    exporter = Exporter()
    print(exporter.exportPath())