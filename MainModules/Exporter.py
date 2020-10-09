# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:14 2020

@author: Julian
"""
import re
import datetime
import pathlib
import xlsxwriter
from PyQt5 import QtGui

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
        a refenrence to a valid CustomSqlModel representing the three parts of
        a trainingroutine:
            - the trainingroutine itself (routineModel)
            - the trainingalternatives (alternativeModel)
            - the trainingnotes (noteModel)
        to use <dataFromModel> all three models have to be set via thier setter
        methods:
            - setRoutineModel()
            - setAlternativeModel()
            - setNoteModel()
        Note: its easier to use <dataFromDatabase>, therefore only a valid
        database (representing a trainingroutine) has to be set via
        <setDatabase>

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
        >>> exporter.setExportPath(...)
        >>> exporter.setName(...)
        >>> exporter.setRoutineName(...)
        >>> exporter.setTrainingPeriode(...)
        >>> exporter.setTrainingMode(...)

    Database Approach:
        >>> exporter.setDatabase(...)

    Model Approach not recommended (use the database approach instead):
        >>> exporter.setRoutineModel(...)
        >>> exporter.setAlternativeModel(...)
        >>> exporter.setNoteModel(...)


    3. export the trainingroutine to a .xlsx-file
        >>> exporter.export()

    """

    def __init__(self,
                 database = None,
                 exportPath = None,
                 name = None,
                 routineName = None,
                 startDate = None,
                 trainingMode = None,
                 workBook = None,
                 routineModel = None,
                 alternativeModel = None,
                 noteModel = None):

        self._database = None
        self._databaseName = None
        self._databasePath = None
        self._exportPath = None
        self._name = None
        self._routineName = None
        self._trainingPeriode = list()
        self._trainingMode = None
        self._workBook = None
        self._workSheet = None
        self._routineModel = None
        self._alternativeModel = None
        self._noteModel = None
        self._layoutProperties = {
                "headerStartRow": 0,
                "routineStartRow": int(),
                "alternativeStartRow": int(),
                "layoutMaxRows": 40,
                "layoutMaxCols": 10
            }

        if (database):
            self.setDatabase(database)
        if (exportPath):
            self.setExportPath(exportPath)
        if (name):
            self.setName(name)
        if (routineName):
            self.setRoutineName(routineName)
        if (isinstance(startDate, tuple)) and (len(startDate) == 3):
            self.setTrainingPeriode(
                    startDate[0],
                    startDate[1],
                    startDate[2]
                )
        if (trainingMode):
            self.setTrainingMode(trainingMode)
        if (workBook):
            self.setWorkBook(workBook)
        if (routineModel):
            self.setRoutineModel(routineModel)
        if (alternativeModel):
            self.setAlternativeModel(alternativeModel)
        if (noteModel):
            self.setNoteModel(noteModel)

    def alternativeModel(self):
        """
        getter method for the attribute 'alternativeModel'

        Returns
        -------
        CustomSqlModel or QtGui.QStandardItemModel

        """
        return self._alternativeModel

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
        'pathlib.Path(database).stem'

        Returns
        -------
        str
            databaseName.

        """

        return self._databaseName

    def databasePath(self):
        """
        holds the directory of 'databaseName'. this property is written by
        'setDatabase'. it is the equivalent of invoking str(pathlib.Path(database).parent)

        Returns
        -------
        str
            databasePath.

        """

        return self._databasePath

    def dataFromDatabase(self, database = None):
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

        Raises
        ------
        TypeError
            will be raised, if no valid value for the database-property
            has been set.

        Returns
        -------
        routineData : list
            all data from training_routine  as nested list.

        alternativeData : list
            all data from training_alternatives as nested list.

        informationData : list
            all data from general_information as nested list.

        """

        if database:
            self.setDatabase(database)

        if not self.database():
            raise TypeError(
                    "before fetching data from a database, set a path to a valid database-file"
                )
        databaseObj = db.database(self.database())
        routineData = databaseObj.data("training_routine")
        alternativeData = databaseObj.data("training_alternatives")
        noteData = databaseObj.data("training_notes")

        return routineData, alternativeData, noteData

    def dataFromModel(
                self,
                routineModel = None,
                alternativeModel = None,
                noteModel = None):
        """
        retrieve data from different Models as source for routine-data,
        alternative-data and note-data and returns the data as lists.

        Parameters
        ----------
        routineModel : CustomSqlModel or QtGui.QStandardItemModel, optional
            data source for routine data. The default is None.

        alternativeModel : CustomSqlModel or QtGui.QStandardItemModel, optional
            data source for alternative data. The default is None.

        noteModel : CustomSqlModel or QtGui.QStandardItemModel, optional
            data source for model data. The default is None.

        Raises
        ------
        TypeError
            will be raised, if the values for the properties does not match
            <CustomSqlModel> or <QtGui.QStandardItemModel>.
            EXCEPTION: noteModel must explicitly be <QtGui.QStandardItemModel>

        Returns
        -------
        routineData : list
            all data from the routineModel as nested list.

        alternativeData : list
            all data from the alternativeModel as nested list.

        noteData : list
            all data from the noteModel as nested list.

        """

        if routineModel:
            self.setRoutineModel(routineModel)
        if alternativeModel:
            self.setAlternativeModel(alternativeModel)
        if noteModel:
            self.setNoteModel(noteModel)

        if (not isinstance(self.routineModel(), CustomSqlModel)) and \
            (not isinstance(self.routineModel(), QtGui.QStandardItemModel)):
            raise TypeError(
                    "before fetching data from a model, a valid model has to be set for 'routineModel'"
                )
        if (not isinstance(self.alternativeModel(), CustomSqlModel)) and \
            (not isinstance(self.alternative(), QtGui.QStandarItemModel)):
            raise TypeError(
                    "before fetching data from a model, a valid model has to be set for 'alternativeModel'"
                )
        if (not isinstance(self.noteModel(), QtGui.QStandardItemModel)):
            raise TypeError(
                    "before fetching data from a model, a valid model has to be set for 'noteModel'"
                )

        # retrieve routine Data
        rows = self.routineModel().rowCount()
        cols = self.routineModel().columnCount()
        routineData = list()
        for row in range(rows):
            line = []
            for col in range(cols):
                item = self.routineModel().item(row, col)
                line.append(item.userData())
            routineData.append(line)

        # retrieve alternative Data
        rows = self.alternativeModel().rowCount()
        cols = self.alternativeModel().columnCount()
        alternativeData = list()
        for row in range(rows):
            line = []
            for col in range(cols):
                item = self.alternativeModel().item(row, col)
                line.append(item.userData())
            alternativeData.append(line)

        # retrieve note Data
        rows = self.noteModel().rowCount()
        cols = self.noteModel().columnCount()
        noteData = list()
        for row in range(rows):
            line = []
            for col in range(cols):
                item = self.noteModel().item(row, col)
                line.append(item.userData())
            noteData.append(line)
        return routineData, alternativeData, noteData

    def exportPath(self):
        """
        holds the directory-path where to store the exportfile

        Returns
        -------
        str
            exportPath.

        """

        return self._exportPath

    def layoutProperties(self):
        """
        returns the layout properties of the export .xlsx-file.

        Returns
        -------
        dict

        """
        return self._layoutProperties

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

    def noteModel(self):
        """
        getter method for the attribute 'noteModel'

        Returns
        -------
        QtGui.QStandardItemModel

        """
        return self._noteModel

    def export(self):
        """
        export a database representing a trainingroutine to a .xlsx-file.

        if the data should be recieved from the database itself, make sure that
        this database has been set via Exporter.setDatabase.

        if the data should be recieved from a certain datamodel representing a
        database, make sure this datamodel has been set via setter method of all
        three datamodels:
            - setAlternativeModel
            - setRoutineModel
            - setNoteModel

        The common case is just to set a adequat database via <setDatabase> and
        use <dataFromDatabase> further on.

        Note:
        if no proper values either for the database-property nor the
        workBook-property have been set, a ValueError will be raised

        Raises
        ------
        TypeError
             - will be raised if the input is not type list or type tuple, or the
               'workBook' property does not hold a valid 'xlsxwriter.Workbook' object

        Returns
        -------
        None.

        """

        """ set the export procedure properties"""
        path = self.exportPath() / pathlib.Path(self.routineName())
        workbook = xlsxwriter.Workbook(path)
        self.setWorkBook(workbook)

        """ layout the export file"""
        worksheet, layoutInformation = exporterUtils.layoutTemplate(self)
        props = {
            "headerStartRow": layoutInformation["headerStartRow"],
            "routineStartRow": layoutInformation["routineStartRow"],
            "layoutMaxRows": layoutInformation["layoutMaxRows"],
            "layoutMaxCols": layoutInformation["layoutMaxCols"]
        }
        self.setLayoutProperties(props)
        self.setWorkSheet(worksheet)

        """populate the export file with training-data"""
        layoutInformation = exporterUtils.populateTemplate(self)
        props = {
                "alternativeStartRow": layoutInformation["alternativeStartRow"]
            }
        self.setLayoutProperties(props)

        """export the file"""
        self.workBook().close()

    def routineModel(self):
        """
        holds a reference to a vild CustomSqlModel representing routine-data
        of a trainingroutine

        Returns
        -------
        CustomSqlModel

        """
        return self._routineModel

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

    def setAlternativeModel(self, model):
        """
        setter method for the attribute 'alternativeModel'

        Parameters
        ----------
        model : CustomSqlModel or QtGui.QStandardItemModel

        Raises
        ------
        TypeError
            will be raised, if <model> does not match <CustomSqlModel> or <QtGui.QStandardItemModel>.

        Returns
        -------
        None.

        """
        if (not isinstance(model, QtGui.QStandardItemModel)) and (not isinstance(model, CustomSqlModel)):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(model),
                            type_name_1 = QtGui.QStandardItemModel,
                            type_name_2 = CustomSqlModel
                        )
                )

        self._alternativeModel = model

    def setDatabase(self, databasePath):
        """
        setter method for the 'database'-property.

        Parameters
        ----------
        databasePath : str; pathlib.Path()
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

        if not isinstance(databasePath, str) and not isinstance(databasePath, pathlib.Path):
            raise TypeError(
                    "input <{input_value}> for argument 'databasePath' does not match {type_name}".format(
                            input_value = databasePath,
                            type_name = type("str")
                        )
                )
        path = pathlib.Path(databasePath)
        if not path.exists():
            raise ValueError(
                    "Database does not exist: {input_name}".format(
                            input_name = str(path)
                        )
                )
        if path == pathlib.Path():
            raise ValueError(
                    "invalid input for argument 'databasePath'"
                )
        self._database = path
        self._databaseName = path.stem
        self._databasePath = path.parent
        self.setRoutineName(path.stem + ".xlsx")

    def setExportPath(self, exportPath):
        """
        setter method for the 'exportPath'-property.

        Parameters
        ----------
        exportPath : str, pathlib.Path
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


        if (not isinstance(exportPath, str)) and (not isinstance(exportPath, pathlib.Path)):
            raise TypeError(
                    "input for argument 'exportPath' does not match {type_name} or {type_name_2}".format(
                            type_name = pathlib.Path,
                            type_name_2 = str
                        )
                )
        path = pathlib.Path(exportPath)
        if not path.is_dir():
            raise ValueError(
                    "input for argument 'exportPath' does not refer to an existing directory"
                )
        if path == pathlib.Path():
            raise ValueError(
                    "invalid input for argument 'exportPath'"
                )
        self._exportPath = path

    def setLayoutProperties(self, props):
        if not isinstance(props, dict):
            raise TypeError(
                    "input for argument 'props' does not match {type_name}".format(
                            type_name = dict
                        )
                )
        for key in props:
            if key in self._layoutProperties:
                if key == "layoutMaxRows":
                    if props[key] <= 40:
                        print("The number of maximum Rows in a Trainingroutine is not allowed to be less then 40.")
                        props[key] = 40
                if key == "layoutMaxCols":
                    if props[key] != 10:
                        print("The number of maximum columns in a Trainingroutine should stay at 10.")
                        props[key] = 10
                self._layoutProperties[key] = props[key]

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
                    "input {input_name} for 'setModel' does not match {type_name}".format(
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

        if not isinstance(name, str):
            raise TypeError(
                "input <{name}> does not match {type_name}".format(
                        name = str(name),
                        type_name = str,
                    )
                )
        if len(name) == 0:
            raise ValueError("empty input for the attribute 'name'")

        self._name = name

    def setNoteModel(self, model):
        """
        setter method for the attribute 'noteModel'

        Parameters
        ----------
        model : QtGui.QStandardItemModel

        Raises
        ------
        TypeError
            will be raised if <model> is not type <QtGui.QStandardItemModel>.

        Returns
        -------
        None.

        """
        if (not isinstance(model, QtGui.QStandardItemModel)) and (not isinstance(model, CustomSqlModel)):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(model),
                            type_name_1 = QtGui.QStandardItemModel,
                            type_name_2 = CustomSqlModel
                        )
                )

        self._noteModel = model

    def setRoutineModel(self, model):
        """
        set the attribute 'routineModel' to <model>

        Parameters
        ----------
        model : CustomSqlModle, QtGui.QStandartItemModel

        Raises
        ------
        TypeError
            will be raised if <model> is not type 'CustomSqlModel' or 'QtGui.QStandardItemModel'

        Returns
        -------
        None.

        """
        if (not isinstance(model, QtGui.QStandardItemModel)) and (not isinstance(model, CustomSqlModel)):
            raise TypeError(
                    "input <{input_name}> does not match {type_name}".format(
                            input_name = str(model),
                            type_name = QtGui.QStandardItemModel
                        )
                )

        self._routineModel = model

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
            will be raised if 'routineName' is not string type.
        ValueError
            will be raised if 'routineName' is an empty string.

        Returns
        -------
        None.

        """

        if not isinstance(routineName, str):
            raise TypeError(
                "input argument {name} does not match {type_name}".format(
                        name = routineName,
                        type_name = str
                    )
                )
        if len(routineName) == 0:
            raise ValueError("empty input for the attribute 'routineName'")

        match = re.search(r"(?P<baseName>\w+).*\w*", routineName)
        if match:
            routineName = match.group("baseName") + ".xlsx"
            self._routineName = routineName
        else:
            if self.databaseName():
                routineName = self.databaseName() + ".xlsx"
                self._routineName = routineName
            else:
                self._routineName = None

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

    def setTrainingPeriode(self, startYear, startMonth, startDay,
                           endYear = None, endMonth = None, endDay = None):
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

        if endYear and endMonth and endDay:
            endDate = datetime.date(endYear, endMonth, endDay)
        else:
            endDate = startDate + datetime.timedelta(days = 42)
        startDateString = startDate.strftime("%d.%m.%Y")
        endDateString = endDate.strftime("%d.%m.%Y")
        self._trainingPeriode = [startDateString, endDateString]

    def setWorkBook(self, workBook):
        """
        setter method for the 'workBook'-property. this property is normally
        not meant to be set manually, because it will be set by <routineLayout>.
        However, for convinience of special cases it is possible to modify the
        value of 'workBook' later on

        Parameters
        ----------
        workBook : xlsxwriter.Workbook
            workbook objects will used as intermediate to create the exportfile.

        Raises
        ------
        TypeError
            will be raised, if the paramter is not type openpyxl.Workbook.

        Returns
        -------
        None.

        """

        if not type(workBook) == xlsxwriter.Workbook:
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'xlsxwriter.Workbook' module"
                )
        self._workBook = workBook

    def setWorkSheet(self, worksheet):
        """
        setter method for the 'workSheet'-property. this property is going to be
        set automatically by invoking the <routineLayout> method.
        However, for convinience of special cases it is possible to modify the
        value of 'workSheet' later on
        Parameters
        ----------
        worksheet : xlsxwriter.worksheet.Worksheet

        Raises
        ------
        TypeError

            - will be raised, if the input for 'worksheet' is not type <xlsxwriter.worksheet.Worksheet>

        Returns
        -------
        None.

        """
        if not isinstance(worksheet, xlsxwriter.worksheet.Worksheet):
            raise TypeError(
                    "input for 'workBook' must be an instance of the 'xlsxwriter.worksheet.Worksheet' module"
                )
        self._workSheet = worksheet

    def workBook(self):
        """
        holds the intermediate workbook-object which will be needed to create
        the export file

        Returns
        -------
        xlsxwriter.Workbook
        """

        return self._workBook

    def workSheet(self):
        """
        getter method for the 'worksheet'-property. the worksheet is related
        to the workBook property.

        Returns
        -------
        <xlsxwriter.worksheet.Worksheet>
        """
        return self._workSheet

if __name__ == "__main__":
    file = pathlib.Path(r"C:\Users\Surface\Documents\Trainingspläne\Datenbanken\Training-200829.db")
    print("file: {}".format(file))
    print("Existing: {}".format(file.is_file()))

    exporter = Exporter()
    exporter.setDatabase(file)
    exporter.setExportPath("C:/Users/Surface/Documents/Python/Projekte/Aphrodite/Aphrodite/files/test_files")
    exporter.setName("Julian Blaser")
    exporter.setTrainingMode("mittleres Krafttraining")
    exporter.setTrainingPeriode(2020, 10, 6)
    print("Export-Path: {}".format(exporter.exportPath()))
    print("Export-Name: {}".format(exporter.databaseName()))
    print("Full Database-Name: {}".format(exporter.database().name))

    exporter.export()
    print("Workbook: {}".format(exporter.workBook()))
    print("Worksheet: {}".format(exporter.workSheet()))