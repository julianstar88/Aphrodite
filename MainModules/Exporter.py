# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:14 2020

@author: Julian
"""
import datetime
import pathlib2
import openpyxl
import numpy as np
import MainModules.Database as db
import UtilityModules.ExporterUtilityModules as exporterUtils
from UtilityModules.CustomModel import CustomSqlModel

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

    - model:
        a refenrence to a valid CustomSqlModel

        - default: None
        - getter: model()
        - setter: setModel(model)

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
        automatically six weeks later. the getter will return a list consisting
        of strings describing the start date in first place and the end date in
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

        >>> exporter = Exporter()

    2. set suitable properties:

        >>> exporter.setDatabase(...)
        >>> exporter.setExportPath(...)
        >>> exporter.setName(...)
        >>> exporter.setTrainingPeriode(...)
        >>> exporter.setTrainingMode(...)

    3. layout the exportfile:

        >>> exporter.routineLayout()

    4. populate the exportfile with exercises, sets and repetitions

        >>> exporter.populateRoutine()

    5. save the workBook to create the exportfile

        >>> exporter.saveRoutine()

    """
    def __init__(self,
                 database = None,
                 exportPath = None,
                 model = None,
                 name = None,
                 routineName = None,
                 trainingPeriode = [None, None],
                 trainingMode = None,
                 workBook = None):

        self._database = database
        self._databaseName = None
        self._databasePath = None
        self._exportPath = exportPath
        self._model = None
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
        'setDatabase'. it is the equivalent of invoking
        'pathlib2.Path(database).stem'

        Returns
        -------
        str
            databaseName.

        """

        return self._databaseName

    def databasePath(self):
        """
        holds the directory of 'databaseName'. this property is written by
        'setDatabase'. it is the equivalent of invoking str(pathlib2.Path(database).parent)

        Returns
        -------
        str
            databasePath.

        """

        return self._databasePath

    def dataFromDatabase(self, database = None, tableName = "training_routine"):
        """
        retrieve data from a database as source for training data. the property
        'database' can be st either by calling 'setDatabase' or directly by
        calling 'dataFromDatabase(database)' with a path to a valid database-file.
        additionally, one can set the tabel from wich to retrive data, by setting
        the 'tableName' argument to a valid table.

        Parameters
        ----------
        database : str, optional
            path to a valid database-file. The default is None.
        tableName : str, optional
            name of a table in database. The default is "training_routine".

        Raises
        ------
        TypeError
            will be raised, if no valid value for the database-property
            has been set.

        Returns
        -------
        data : list
            all data within a database as nested list.

        """

        if database:
            self.setDatabase(database)

        if not self.database():
            raise TypeError(
                    "before fetching data from a database, set a path to a valid database-file"
                )
        pathObj = pathlib2.Path(self.database())
        databaseName = pathObj.stem
        databaseObj = db.database(pathObj.parent)
        data = databaseObj.data(tableName, databaseName)

        return data

    def dataFromModel(self, model = None):
        """
        retrieve data from a CustomSqlModel as source for training data. the property
        'mdoel' can be st either by calling 'setModel' or directly by
        calling 'dataFromModel(model)' with a reference to a valid CustomSqlModel.

        Parameters
        ----------
        model : CustomSqlModel, optional
            reference to a valid CustomSqlModel. The default is None.

        Raises
        ------
        TypeError
            will be raised, if no valid value for the 'model' property has been set.

        Returns
        -------
        modelData : list
            all data in a CustomSqlModel as nested list.

        """

        if model:
            self.setModel(model)

        if not isinstance(self.model(), CustomSqlModel):
            raise TypeError(
                    "before fetching data from a model, a valid <QStandardItemModel> has to be set for the model-property of 'GraphicalEvaluator'"
                )

        rows = self.model().rowCount()
        cols = self.model().columnCount()

        modelData = []
        for row in range(rows):
            line = []
            for col in range(cols):
                item = self.model().item(row, col)
                line.append(item.userData())
            modelData.append(line)
        return modelData

    def exportPath(self):
        """
        holds the directory-path where to store the exportfile

        Returns
        -------
        str
            exportPath.

        """

        return self._exportPath

    def model(self):
        """
        holds a reference to a valid CustomSqlModel-object

        Returns
        -------
        CustomSqlModel

        """

        return self._model

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

    def populateRoutine(self, data):
        """
        by invoking this method, the workbook in the 'workBook' property gets
        populated with data from the database. make sure, that 'routineLayout'
        has been invoked prior.
        if no proper values either for the database-property or the
        workBook-property have been set, a ValueError will be raised

        Parameters
        ----------
        databasePath : str
            this parameter must point to a valid db-file
            (typically a trainingroutine).

        Raises
        ------
        TypeError
             will be raised if the input is not type list or type tuple, or the
             'workBook' property does not hold a valid 'openpyxl.Workbook' object

        ValueError
            will be raised, if the 'database' property does not point to a valid
            database-file. it will also be raised, if the dimension of the
            'numpy.array' representation of data does not match (n, m)

        Returns
        -------
        None.

        """
        if not isinstance(data, tuple) and not isinstance(data, list):
            raise TypeError(
                    "input {input_type} does not match {expected_type_1} nor {expected_type_2}".format(
                            input_type = type(data),
                            expected_type_1 = tuple,
                            expected_type_2 = list
                        )
                )
        if not len(np.array(data).shape) == 2:
            raise ValueError(
                    "dim = {input_dim} for argument 'data' does not match the expected dim = 2".format(
                            input_dim = str(len(np.array(data).shape))
                        )
                )

        if not self.database():
            raise ValueError(
                    "tried to access an invalid database. set a vild Database.database-object as database, before populating a trainingroutine"
                )

        if not isinstance(self.workBook(), openpyxl.Workbook):
            raise TypeError(
                    "tried to access an invalid workbook. set a valid openpyxl.Workbook-object as workbook, before populating a trainingroutine "
                )

        ws = self.workBook().active

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
        """
        save the intermediate workbook 'workBook' and create the final export-
        file (.xlsx-file). the exportfile will be saved to the 'exportPath',
        with the name 'routineName'. to prevent unexpected behavior, one should
        obey the recommended procedure in the class-documentation.

        Raises
        ------
        TypeError
            will be raised, if either 'exportPath' or 'routineName' are
            invalid.

        Returns
        -------
        None.

        """


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
        """
        setter method for the 'database'-property.

        Parameters
        ----------
        databasePath : str
            this parameter must point to a valid db-file
            (typically a trainingroutine).

        Raises
        ------
        TypeError
             will be raised if the input is not type str.

        ValueError
            will be raised if input is an empty string or a path which
            does not point to a file.

        Returns
        -------
        None.

        """

        if not isinstance(databasePath, str):
            raise TypeError(
                    "input {input_value} for argument 'databasePath' does not match {type_name}".format(
                            input_value = databasePath,
                            type_name = type("str")
                        )
                )
        path = pathlib2.Path(databasePath)
        if not path.exists():
            raise ValueError(
                    "Database does not exist: {input_name}".format(
                            input_name = str(path)
                        )
                )
        if len(databasePath) == 0:
            raise ValueError(
                    "invalid input for argument 'databasePath'"
                )
        self._database = str(path)
        self._databaseName = path.stem
        self._databasePath = path.parent

    def setExportPath(self, exportPath):
        """
        setter method for the 'exportPath'-property.

        Parameters
        ----------
        exportPath : str
            exportPath must point to a directory, where the exportfile
            will be stored.

        Raises
        ------
        TypeError
            will be raised, if the input is not type str.

        ValueError
            will be raised, if the input does not point to a directory,
            or the length of the input string is zeor.

        Returns
        -------
        None.

        """

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

    def setModel(self, model):
        """
        setter method for the property: model

        Parameters
        ----------
        model : CustomSqlModel
            valid reference to a CustomSqlModel-object.

        Raises
        ------
        TypeError
            will be raised, if model is no CustomSqlModel-type.

        Returns
        -------
        None.

        """

        if not isinstance(model, CustomSqlModel):
            raise TypeError(
                    "input <{input_name}> for 'setModel' does not match {type_name}".format(
                            input_name = type(model),
                            type_name = CustomSqlModel
                        )
                )

        self._model = model

    def setName(self, name):
        """
        setter methof for the 'name'-property.

        Parameters
        ----------
        name : str
            Username, written in the exportfile.

        Raises
        ------
        TypeError
            will be raised, if the input is not type str.

        ValueError
            will be raised, if the length of the input is zero.

        Returns
        -------
        None.

        """

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
        """
        setter method for the 'routineName'-property

        Parameters
        ----------
        routineName : str
            this represents the name of the exporfile.

        Raises
        ------
        TypeError
            will be raised.
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """

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
        """
        setter for the 'trainingMode'-property

        Parameters
        ----------
        trainingMode : str
            descirbes which the type of training. this property will be written
            inot the exportfile.

        Raises
        ------
        TypeError
            will be raised, if the input is not type str.
        ValueError
            will be raised, if input length is zero.

        Returns
        -------
        None.

        """

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
        """
        setter method for the 'trainingPeriode'-property. the setter provides
        only the possibility to set the start date. the end date will be
        computed automatically six weeks later.

        Parameters
        ----------
        startYear : int
            start year of the training.
        startMonth : int
            start month of the training.
        startDay : int
            start day of the training.

        Raises
        ------
        TypeError
            will be raised, if one of the parameters is not type int.

        Returns
        -------
        None.

        """

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
        """
        setter method for the 'workBook'-property. this property is normally
        not meant to be set manually, because it will be set by 'setDatabase'.
        However, for convinience of special cases it is possible to modify the
        value of the 'workBook' later on

        Parameters
        ----------
        workBook : openpyxl.Workbook
            workbook objects will used as intermediate to create the exportfile.

        Raises
        ------
        TypeError
            will be raised, if the paramter is not type openpyxl.Workbook.

        Returns
        -------
        None.

        """

        if not type(workBook) == openpyxl.Workbook:
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'openpyxl.Workbook' module"
                )
        self._workBook = workBook

    def workBook(self):
        """
        holds the intermediate workbook-object which will be needed to create
        the export file

        Returns
        -------
        openpyxl.Workbook
            the 'workBook'-property.

        """

        return self._workBook

if __name__ == "__main__":
    pass