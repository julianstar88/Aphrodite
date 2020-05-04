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
        if parentWidget:
            self.setParentWidget(parentWidget)

        if not self.parentWidget():
            raise TypeError(
                    "before connecting the 'GraphicalEvaluator' to a Parent, the parentWidget have to be set to a <PyQt5.QtWidgets.QWidget> object"
                )
        self.parentWidget().setLayout(self._layout)

    def database(self):
        return self._database

    def dataFromDatabase(self, database = None, tableName = "training_routine"):
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
        if isinstance(mainWidget, QtWidgets.QTabWidget):
            self._mainWidget = mainWidget
        else:
            self._mainWidget = QtWidgets.QTabWidget()

        self._mainWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self._layout.addWidget(self._mainWidget)

    def mainWidget(self):
        return self._mainWidget

    def model(self):
        return self._model

    def parentWidget(self):
        return self._parentWidget

    def plotData(self, data):
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
        if not isinstance(model, CustomSqlModel):
            raise TypeError(
                    "input <{input_name}> for 'setModel' does not match {type_name}".format(
                            input_name = str(model),
                            type_name = CustomSqlModel
                        )
                )

        self._model = model

    def setParentWidget(self, parentWidget):
        if not isinstance(parentWidget, QtWidgets.QWidget):
            raise TypeError(
                    "input <{input_name}> for 'setParentWidget' does not match {type_name}".format(
                            input_name = str(parentWidget),
                            type_name = QtWidgets.QWidget
                        )
                )

        self._parentWidget = parentWidget

class EvaluatorTab(QtWidgets.QWidget):

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
        # self.canvas = FigureCanvas(self.fig)
        # self.layout.addWidget(self.canvas)

        # x = np.linspace(1,6,6)
        # y = self.readData(data[4:])
        # self.ax.plot(x,y)

        # labels = ["Week " + str(i) for i in range(0,7,1)]
        # self.ax.set_xticklabels(labels)

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

        self._data = self.__readData(data[4:])


if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            super().__init__(*args)
            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Graphical Evaluator Test")

            database = pathlib2.Path("examples/Qt_ModelView/database/test_database.db")
            parentDir = pathlib2.Path().cwd().parent
            model = CustomSqlModel(
                database = parentDir / database,
                table = "training_routine",
                tableStartIndex = 0,
                valueStartIndex = 5
            )
            model.populateModel()

            self.evaluator = GraphicalEvaluator()
            self.evaluator.initiateQWidgets()
            self.evaluator.setModel(model)
            self.evaluator.setDatabase(str(parentDir / database))
            self.evaluator.connectEvaluator(self.main)
            self.evaluator.createTabs([[1,2,3]])
            # self.evaluator.createTabs(self.evaluator.dataFromDatabase())
            self.evaluator.plotData(self.evaluator.dataFromDatabase())

            self.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())