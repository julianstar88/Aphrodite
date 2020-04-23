# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:14 2020

@author: Julian
"""
import datetime
import pathlib2
import openpyxl
import os.path
import MainModules.Database as db
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

        self._database = database
        self._databaseName = None
        self._databasePath = None
        self._exportPath = exportPath
        self._name = name
        self._routineName = routineName
        self._trainingPeriode = trainingPeriode
        self._trainingMode = trainingMode
        self._workBook = workBook

    def database(self):
        return self._database

    def databaseName(self):
        return self._databaseName

    def databasePath(self):
        return self._databasePath

    def exportPath(self):
        return self._exportPath

    def name(self):
        return self._name

    def populateRoutine(self):
        if not self.database():
            raise TypeError(
                    "tried to access an invalid database. set a vild Database.database-object as database, before populating a trainingroutine"
                )

        if not self.workBook():
            raise TypeError(
                    "tried to access an invalid workbook. set a valid openpyxl.Workbook-object as workbook, before populating a trainingroutine "
                )

        ws = self.workBook().active
        database = db.database(self.databasePath())
        data = database.data(self.databaseName(), "training_routine")

        ws["A3"] = self.name()
        ws["F3"] = self.trainingPeriode()[0]
        ws["F4"] = self.trainingPeriode()[1]
        ws["I3"] = self.trainingMode()

        inputValues = [data[i][0] for i in range(len(data))]
        for i, val in enumerate(inputValues):
            ws["A" + str(7 + i)] = val

        inputValues = [data[i][1] for i in range(len(data))]
        for i, val in enumerate(inputValues):
            ws["C" + str(7 + i)] = val

        inputValues = [data[i][2] for i in range(len(data))]
        for i, val in enumerate(inputValues):
            ws["D" + str(7 + i)] = val

    def routineLayout(self, rows = 40):
        workBook = exporterUtils.TamplateLayout(rows)
        self.setWorkBook(workBook)
        return workBook

    def routineName(self):
        return self._routineName

    def trainingMode(self):
        return self._trainingMode

    def trainingPeriode(self):
        return self._trainingPeriode

    def saveRoutine(self):
        if not self.exportPath():
            raise TypeError (
                    "try to export a trainingroutine to an invalid path. set a valid export path before saving a trainingroutine"
                )

        if not self.routineName():
            raise TypeError(
                    "try to export a trainingroutine with invalid routine name. set a valid routine name before saving a trainingroutine"
                )
        path = pathlib2.Path(self.exportPath()) / pathlib2.Path(self.routineName())
        self.workBook().save(str(path))

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
        self._database = str(path)
        self._databaseName = os.path.splitext(path.name)[0]
        self._databasePath = path.parent

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
        self._exportPath = str(path)

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
            self._name = name

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
            self._routineName = routineName

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
        self._trainingMode = trainingMode

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
        self._trainingPeriode = (startDateString, endDateString)

    def setWorkBook(self, workBook):
        if not type(workBook) == openpyxl.Workbook:
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'openpyxl.Workbook' module"
                )
        self._workBook = workBook

    def workBook(self):
        return self._workBook

if __name__ == "__main__":
    pathObj = pathlib2.Path("test_database.db")
    exporter = Exporter()
    exporter.populateRoutine()