# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:42 2020

@author: Julian
"""
import sys
import pathlib2
from PyQt5 import QtWidgets
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
            self.setDataSource(dataSource)
        else:
            self._dataSource = 0

        self._mainWidget = QtWidgets.QTabWidget()
        self._mainWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._mainWidget)

    def createTabs(self):
        pass

    def database(self):
        return self._database

    def dataSource(self):
        return self._dataSource

    def dataFromDatabase(self):
        pass

    def dataFromModel(self):
        pass

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

    def __init__(self, mainWidget, data):
        super().__init__()
        self.mainWidget = mainWidget
        self.data = data
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

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

            self.evaluator = GraphicalEvaluator()

            self.evaluator.setDataSource("test")

            self.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())