# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:42 2020

@author: Julian
"""
import sys
import pathlib2
import numpy as np
import matplotlib.pyplot as plt
import MainModules.Database as db
from PyQt5 import QtWidgets
from UtilityModules.CustomModel import CustomSqlModel
from UtilityModules.MiscUtilities import ModelInputValidation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphicalEvaluator():
    """
    the GraphicalEvaluator-class serves as interface for plotting the training
    progress as a graphical tool for the training evaluation. it is only possible
    to use this class in the scope of a QApplication from PyQt5, hence it is meant
    to be used in the framework of Aphrodite.

    Properties
    ----------

    - database:
        a path to a existing database file, which is a valid trainingroutine

        - default: None
        - getter: database()
        - setter: setDatabase()

    - mainWidget:
        represents the QTabWidget, which hold the plotted training data in each
        tab

        - default: QTabWidget
        - getter: mainWidget()
        - setter: this property has no setter-method

    - model:
        this property holds a reference to a valid CustomSqlModel-object

        - default: None
        - getter: model()
        - setter: setModel(CustomSqlModel)

    - parentWidget:
        this property holds a reference to a widget in the main app. it serves
        as interface between the GraphicalEvaluator-object and Aphrodite

        - default: None
        - getter: parentWidget()
        - setter: setParentWidget(QWidget)

    Example Usage
    -------------
    1. instantiation of GraphicalEvaluator

        >>> evaluator = GraphicalEvaluator()

    2. adjust settings of the GraphicalEvaluator-object

        >>> evaluator.setModel(model)
        >>> evaluator.setDatabase(database)

    ::

        Note: to plot training data, one can choose between the
        data model or the database as source. it is recommended
        to set both properties with the corresponding setter methods
        and choose one of the method 'dataFromModel' or
        'dataFromDatabase' while creating tabs or data plotting

    3. connect the GraphicalEvaluator-object to the to a parent widget (e.g. the Gui of Aphrodite)

        >>> evaluator.connectEvaluator(parentWidget)

    4. initiate all necessary QWidgets

        >>> evaluator.initiateQWidgets()

    5. create tabs (eihter from database or from model)

        >>> evaluator.createTabs(evaluator.dataFromModel())
        or
        >>> evaluator.createTabs(evaluator.detaFromDatabase())

    6. plot the training data (either form database or from model)

        >>> evaluator.plotData(evaluator.dataFromDatabase())
        or
        >>> evaulator.plotData(evaluator.dataFromModel())

    """
    def __init__(self,
                 database = None,
                 model = None,
                 parentWidget = None):

        if database:
            self.setDatabase(database)
        else:
            self._database = database

        if model:
            self.setModel(model)
        else:
            self._model = model

        if parentWidget:
            self.setParentWidget(parentWidget)
        else:
            self._parentWidget = parentWidget

        self._mainWidget = None
        self._layout = QtWidgets.QVBoxLayout()

    def createTabs(self, data, tabLabels = None):
        """
        create the necessary tabs for data plotting. number of tabs equals
        the length of 'data'. the name of every tab will be the first element
        of each list in data

        Parameters
        ----------
        data : list or tuple
            this parameter represents the training data to be plotted. it has to
            consist of nested lists or tuples in the way, that if its converted
            to a numpy array, would have the shape (n, m).

            e.g. [[1,2,3], [4,5,6], [7,8,9]]

        tabLabels : list or tuple, optional
            holds the label for each tab. if this paremeter
            will be omitted, the labels will be set to the names of each
            exercises. The default is None.

        Raises
        ------
        TypeError
            will be raised, if input is neither a list nor a tuple.
        ValueError
            will be raised if a numpy representation of data does not have
            the shape (n, m).

        Returns
        -------
        None.

        """

        if not isinstance(self.mainWidget(), QtWidgets.QTabWidget):
            raise TypeError(
                    "GraphicalEvaluator.createTabs: set a valid mainWidget before creating Tabs"
                )
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

        if tabLabels:
            labels = tabLabels
        else:
            labels = []
            for row in data:
                labels.append(row[0])

        for i, label in enumerate(labels):
            self.mainWidget().addTab(EvaluatorTab(), label)

    def connectEvaluator(self, parentWidget = None):
        """
        connect a GraphicalEvaluator-object to the parent application. the
        propperty 'parentWidget' can be set either by calling 'setParentWidget()'
        or dricetly by calling 'connectEvaluator(parentWidget)' with a valid
        QWidget as parentWidget

        Parameters
        ----------
        parentWidget : QWidget, optional
            represents the interface to a parent app. The default is None.

        Raises
        ------
        TypeError
            will be raised, if the property 'parentWidget' is not a valid QWidget.

        Returns
        -------
        None.

        """

        if parentWidget:
            self.setParentWidget(parentWidget)

        if not self.parentWidget():
            raise TypeError(
                    "before connecting the 'GraphicalEvaluator' to a Parent, the parentWidget have to be set to a <PyQt5.QtWidgets.QWidget> object"
                )
        self.parentWidget().setLayout(self._layout)

    def database(self):
        """
        getter method for the proerty: database

        Returns
        -------
        str
            path to a database-file.

        """

        return self._database

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
        data = databaseObj.data(databaseName, tableName)

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

        if not self.model():
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

    def initiateQWidgets(self, mainWidget = None):
        """
        set the 'mainWidget' property to a QTabWidget-object. additionaly this
        property can be set directly by setting the 'mainWidget' argument to
        a valid QTabWidget-object

        Parameters
        ----------
        mainWidget : QTabWidget, optional
            a valid reference to a QTabWidget. The default is None.

        Returns
        -------
        None.

        """
        if isinstance(mainWidget, QtWidgets.QTabWidget):
            self._mainWidget = mainWidget
        else:
            self._mainWidget = QtWidgets.QTabWidget()

        self._mainWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self._layout.addWidget(self._mainWidget)

    def mainWidget(self):
        """
        getter method for the property: mainWidget

        Returns
        -------
        QTabWidget

        """

        return self._mainWidget

    def model(self):
        """
        getter method for the property: model

        Returns
        -------
        CustomSqlModel

        """

        return self._model

    def parentWidget(self):
        """
        getter method for the property: parentWidget

        Returns
        -------
        QWidget

        """

        return self._parentWidget

    def plotData(self, data):
        """
        plot the data of a data source into every tab, created by 'createTabs()'

        Parameters
        ----------
        data : list or tuple
            this parameter represents the training data to be plotted. it has to
            consist of nested lists or tuples in the way, that if its converted
            to a numpy array, would have the shape (n, m).

            e.g. [[1,2,3], [4,5,6], [7,8,9]]

        Raises
        ------
        TypeError
            will be raised, if the value of mainWidget is not a valid QTabWidget
            or if 'data' is not an instance of 'lits' or 'tuple'.

        ValueError
            will be raised, if tabs have been created yet, or the numpy
            representation of data does not have the shape (n, m).

        Returns
        -------
        None.

        """

        if not isinstance(self.mainWidget(), QtWidgets.QTabWidget):
            raise TypeError(
                    "before plotting data into tabs, set mainWidget to a valid QTabWidget"
                )
        if self.mainWidget().count() == 0:
            raise ValueError(
                    "befor plotting data into tabs, create tabs in mainWidget using the createTabs() method"
                )
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

        for i in range(self.mainWidget().count()):
            self.mainWidget().widget(i).plotData(data[i])

    def setDatabase(self, database):
        """
        setter method for the property: database

        Parameters
        ----------
        database : str
            path to a valid database.

        Raises
        ------
        TypeError
            if 'database' is not an instance of 'str'.
        ValueError
            if 'database' does not exist, or is not a .db-file.

        Returns
        -------
        None.

        """
        if not isinstance(database, str):
            raise TypeError(
                    "input <{input_name}> for 'setDatabase' does not match {type_name}".format(
                            input_name = str(database),
                            type_name = type("123")
                        )
                )

        pathObj = pathlib2.Path(database)

        if not pathObj.is_file() or pathObj.match(".db"):
            raise ValueError(
                    "input <{input_name}> for 'setDatabase' does not point to an existing database".format(
                            input_name = str(database)
                        )
                )

        self._database = str(pathObj)

    def setModel(self, model):
        """
        setter method for the property: model

        Parameters
        ----------
        model : CustomSqlModel
            reference to a CustomSqlModle-object.

        Raises
        ------
        TypeError
            will be raised, if the argument 'model' is not an instance of
            'CustomSqlModel'.

        Returns
        -------
        None.

        """

        if not isinstance(model, CustomSqlModel):
            raise TypeError(
                    "input <{input_name}> for 'setModel' does not match {type_name}".format(
                            input_name = str(model),
                            type_name = CustomSqlModel
                        )
                )

        self._model = model

    def setParentWidget(self, parentWidget):
        """
        setter method for the property: parentWidget

        Parameters
        ----------
        parentWidget : QWidget
            interface to the parent app.

        Raises
        ------
        TypeError
            will be raised, if 'parentWidget' is not an instance of 'QWidget'.

        Returns
        -------
        None.

        """

        if not isinstance(parentWidget, QtWidgets.QWidget):
            raise TypeError(
                    "input <{input_name}> for 'setParentWidget' does not match {type_name}".format(
                            input_name = str(parentWidget),
                            type_name = QtWidgets.QWidget
                        )
                )

        self._parentWidget = parentWidget

class EvaluatorTab(QtWidgets.QWidget):
    """
    'EvaluatorTab' is a helper class for the 'GraphicalEvaluator'-class and
    thus is not meant to be instantiated by its own. it creats the paiges of every tab
    in 'GraphicalEvaluator' and handles the plotting of the training data

    Properties:
    -----------
    - ax:
        Axes-object for data plotting

    - canvas:
        FigureCanvasQTAgg-object of fig

    - data:
        data to be plotted

    - fig
        Figure-object for data plotting

    - layout:
        QVBoxLayout-object

    """

    def __init__(self, data = None):
        super().__init__()

        if data:
            self.setData(data)
        else:
            self._data = None

        self.canvas = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        self.ax.grid(which = "major")

    def data(self):
        return self._data

    def plotData(self, data = None):
        if data:
            self.setData(data)

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        x = np.linspace(1,6,6)
        y = self.data()
        self.ax.plot(x,y)

        labels = ["Week " + str(i) for i in range(0,7,1)]
        self.ax.set_xticklabels(labels)

    def __readData(self, data):

        validator = ModelInputValidation()
        return [validator.readValue(val)[0] for val in data]

    def setData(self, data):
        if not isinstance(data, tuple) and not isinstance(data, list):
            raise TypeError(
                    "input {input_type} does not match {expected_type_1} nor {expected_type_2}".format(
                            input_type = type(data),
                            expected_type_1 = tuple,
                            expected_type_2 = list
                        )
                )
        if not len(np.array(data).shape) == 1:
            raise ValueError(
                    "dim = {input_dim} for argument 'data' does not match the expected dim = 2".format(
                            input_dim = str(len(np.array(data).shape))
                        )
                )

        self._data = self.__readData(data[4:-1])


if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            super().__init__(*args)
            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Graphical Evaluator Test")

            # database = pathlib2.Path("examples/Qt_ModelView/database/test_database_2.db")
            database = pathlib2.Path("files/test_files/test_database_2.db")
            parentDir = pathlib2.Path().cwd().parent
            model = CustomSqlModel(
                database = parentDir / database,
                table = "training_routine",
                tableStartIndex = 0,
                valueStartIndex = 5
            )
            model.populateModel()

            self.evaluator = GraphicalEvaluator()

            self.evaluator.setModel(model)
            self.evaluator.setDatabase(str(parentDir / database))
            self.evaluator.connectEvaluator(self.main)
            self.evaluator.initiateQWidgets()
            self.evaluator.createTabs(self.evaluator.dataFromDatabase())
            self.evaluator.plotData(self.evaluator.dataFromDatabase())

            self.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())