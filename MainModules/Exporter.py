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
    """
    exports a table from a database to an excel-file (.xlsx). although the
    database can be set arbitrarily, the database is supposed to be a
    training-routine-database.
    this class is meant to be used in the framwork of 'Aphrodite'

    Properties
    ----------
    - database:
        a path to a existing database file, which is a valid trainingroutine

        - default: None
        - getter: database()
        - setter: setDatabase(db-file)

    - exportPath:
        a path to a dirctory to store the created exportfile in

        - default: None
        - getter: exportPath()
        - setter: setExportPath(directory-path)

    - name:
        username for the trainingroutine

        - default: None
        - getter: name()
        - setter: setName(name)

    - routineName:
        name of the exportfile

        - default: None
        - getter: routineName()
        - setter: setRoutineName(routine-name)

    - trainingPeriode:
        discribes the duration for the trainingroutine. One has only to provide
        the start date via the setter method, the end date will be calulated
        automatically six weeks later. the getter will return a tuple consisting
        of strings describing the start data in first place and the end data in
        last place

        - default: None
        - getter: trainingPeriode()
        - setter: setTrainingPeriode(year, month, day)

    - trainingMode:
        describes which kind of trainingform is written into the exportfile

        - default: None
        - getter: trainingMode
        - setter: setTrainingMode(mode)

    - workBook:
        'workBook' is an openpyxl.Workbook object, used to create the exportfile.
        this property gets written, if one set a path to a valid database. it
        also can be changed using its setter method

        - default: none
        - getter: workBook()
        - setter: setWorkBook(workbook)

    Usage
    -----

    1. create the exporter object:

        - exporter = Exporter()

    2. set suitable properties:

        - exporter.setDatabase(...)
        - exporter.setExportPath(...)
        - exporter.setName(...)
        - exporter.setTrainingPeriode(...)
        - exporter.setTrainingMode(...)

    3. layout the exportfile:

        - exporter.routineLayout()

    4. populate the exportfile with exercises, sets and repetitions

        - exporter.populateRoutine()

    5. save the workBook to create the exportfile

        - exporter.saveRoutine()
    """
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
        """
        holds thepath to a existing database file, which is a valid
        trainingroutine. the database is needed to populate the the
        exportfile.


        Returns
        -------
        str
            path to a database.

        """

        return self._database

    def databaseName(self):
        """
        holds the name of the database. this property is written by
        'setDatabase'. it is the equivalent of invoking 'os.path.basename()' and
        'os.path.spiltext()[0]'

        Returns
        -------
        str
            databaseName.

        """

        return self._databaseName

    def databasePath(self):
        """
        holds the directory of 'databaseName'. this property is written by
        'setDatabase'. it is the equivalent of invoking 'os.path.basename()' and
        'os.path.spiltext()[0]'

        Returns
        -------
        str
            databasePath.

        """

        return self._databasePath

    def exportPath(self):
        """
        holds the directory-path where to store the exportfile

        Returns
        -------
        str
            exportPath.

        """

        return self._exportPath

    def name(self):
        """
        holds the username for the trainingroutine. this is the name, which
        will be written under the name in the exportfile

        Returns
        -------
        str
            name.

        """

        return self._name

    def populateRoutine(self):
        """
        by invoking this method, the workbook in the 'workBook' property gets
        populated with data from the database. make sure, that 'routineLayout'
        has been invoked prior.
        if no proper values either for the database-property or the
        workBook-property have been set, a ValueError will be raised

        Returns
        -------
        None.

        """

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
        """
        by invoking this method, the layout for the trainingroutine
        in the exportfile will be created. its also writing the intermediate
        workbook file to the 'workBook'-property. for convinience, the created
        intermediade workbook will be returned to the user.

        Parameters
        ----------
        rows : int, optional
            determines, how many rows in the exportfile will be available.
            The default is 40.

        Returns
        -------
        workBook : openpyxl.Workbook
            intermediate workbook ojbect.

        """

        workBook = exporterUtils.TamplateLayout(rows)
        self.setWorkBook(workBook)
        return workBook

    def routineName(self):
        """
        holds the routinename for the exportfile. this will be the name for the
        -excel-file, which will be saved at 'exportPath'

        Returns
        -------
        str
            routineName.

        """

        return self._routineName

    def trainingMode(self):
        """
        holds the mode, which discribes the kind of training. this mode will be
        written into the exportfile

        Returns
        -------
        str
            trainingMode.

        """

        return self._trainingMode

    def trainingPeriode(self):
        """
        holds the duration for the trainingroutine. the dates in this property
        will be written to the exportfile

        Returns
        -------
        tuple
            contains the start and end date of the given trainingroutine.

        """

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
        self._trainingPeriode = [startDateString, endDateString]

    def setWorkBook(self, workBook):
        if not type(workBook) == openpyxl.Workbook:
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'openpyxl.Workbook' module"
                )
        self._workBook = workBook

    def workBook(self):
        return self._workBook

if __name__ == "__main__":
    pass