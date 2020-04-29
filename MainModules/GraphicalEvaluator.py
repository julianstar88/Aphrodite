# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:42 2020

@author: Julian
"""
import sys
import pathlib2
import MainModules.Database as db
from PyQt5 import QtWidgets
from UtilityModules.CustomModel import CustomSqlModel

class GraphicalEvaluator():

    def __init__(self, database = None, mainWidget = None, model = None, parentWidget = None):

        if database:
            self.setDatabase(database)
        else:
            self._database = database

        if mainWidget:
            self.setMainWidget(mainWidget)
        else:
            self._mainWidget = mainWidget

        if model:
            self.setModel(model)
        else:
            self._model = model

        if parentWidget:
            self.setParentWidget(parentWidget)
        else:
            self._parentWidget = parentWidget

    def createTabs(self):
        pass

    def database(self):
        return self._database

    def getInformation(self):
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
                    "input for 'setDatabase' does not match {type_name}".format(
                            type_name = type("123")
                        )
                )

        pathObj = pathlib2.Path(database)

        if not pathObj.is_file() or pathObj.match(".db"):
            raise ValueError(
                    "input for 'setDatabase' does not point to an existing database"
                )

        self._database = str(pathObj)

    def setMainWidget(self, mainWidget):
        if not type(mainWidget) == QtWidgets.QWidget:
            raise TypeError(
                    "input for 'setMainWidget' does not match {type_name}".format(
                            type_name = QtWidgets.QWidget
                        )
                )

    def setModel(self, model):
        pass

    def setParentWidget(self, parentWidget):
        pass

if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            super().__init__(*args)
            self.main = QtWidgets.QWidget(self)
            self.setCentralWidget(self.main)
            self.setGeometry(100,100,800,500)
            self.setWindowTitle("Graphical Evaluator Test")

            self.evaluator = GraphicalEvaluator()

            self.evaluator.setMainWidget("test")

            self.show()

    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())