# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:42 2020

@author: Julian
"""
import sys
import pathlib2
from PyQt5 import QtWidgets, QtCore
from UtilityModules.CustomModel import CustomSqlModel

class GraphicalEvaluator():

    def __init__(self,
                 database = None,
                 model = None,
                 parentWidget = None,
                 dataSource = None):

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

        if dataSource:
            # 0: data source is model
            # 1: data source is database
            self.setDataSource(dataSource)
        else:
            self._dataSource = 0

        self._mainWidget = QtWidgets.QTabWidget()
        self._mainWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._mainWidget)

    def createTabs(self, tabLabels = None):
        if self.dataSource() == 0:
            data = self.dataFromModel()

        if self.dataSource() == 1:
            data = self.dataFromDatabase()

        print(data)

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

    def dataSource(self):
        return self._dataSource

    def dataFromDatabase(self):
        pass

    def dataFromModel(self, model = None):
        if model:
            self.setModel(model)

        if not self.model():
            raise TypeError(
                    "before fetching data from a model, a valid <QStandardItemModel> has to be set for the model-property of 'GraphicalEvaluator'"
                )

        rows = self.model().rowCount()
        cols = self.model().columnCount()
        print(rows)
        data = []
        for row in range(rows):
            line = []
            for col in range(cols):
                item = self.model().item(row, col)
                line.append(item.data(role = QtCore.Qt.DisplayRole))
            data.append(line)
        return data

    def mainWidget(self):
        return self._mainWidget

    def model(self):
        return self._model

    def parentWidget(self):
        return self._parentWidget

    def setDatabase(self, database):
        if not type(database) == str:
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

    def setDataSource(self, source):
        if not type(source) == int:
            raise TypeError(
                    "input <{input_name}> for 'setDataSource' does not match {type_name}".format(
                            input_name = str(source),
                            type_name = int
                        )
                )
        if not (0 <= source <= 1):
            raise ValueError(
                    "input for 'setDataSource' is not valid"
                )

        self._dataSource = source

    def setModel(self, model):
        if not type(model) == CustomSqlModel:
            raise TypeError(
                    "input <{input_name}> for 'setModel' does not match {type_name}".format(
                            input_name = str(model),
                            type_name = CustomSqlModel
                        )
                )

        self._model = model

    def setParentWidget(self, parentWidget):
        if not type(parentWidget) == QtWidgets.QWidget:
            raise TypeError(
                    "input <{input_name}> for 'setParentWidget' does not match {type_name}".format(
                            input_name = str(parentWidget),
                            type_name = QtWidgets.QWidget
                        )
                )

        self._parentWidget = parentWidget

class EvaluatorTab(QtWidgets.QWidget):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.layout = QtWidgets.QVBoxLayout(self)

        testLabel = QtWidgets.QLabel("test")

        self.layout.addWidget(testLabel)



if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            super().__init__(*args)
            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Graphical Evaluator Test")

            model = CustomSqlModel(
                database = "examples/Qt_ModelView/database/test_database.db",
                table = "training_routine",
                tableStartIndex = 0,
            )

            self.evaluator = GraphicalEvaluator()
            self.evaluator.setModel(model)
            self.evaluator.connectEvaluator(self.main)
            self.evaluator.createTabs()

            self.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())