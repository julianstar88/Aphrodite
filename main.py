# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:59:00 2020

@author: Julian
"""
import sys
import pathlib2
import GuiModules.MainInterface as mi
from MainModules import ConfigInterface, Exporter, GraphicalEvaluator
from UtilityModules import CustomModel
from PyQt5 import QtWidgets

configFile = pathlib2.Path("files/config/config.txt")
parentDir = pathlib2.Path().cwd()
configParser = ConfigInterface.ConfigParser()
configParser.readConfigFile(parentDir / configFile)

database = pathlib2.Path(configParser.readAttributes()["current_routine"])

trainingModel = CustomModel.CustomSqlModel(
        database = str(database),
        table = "training_routine",
        tableStartIndex = 0,
        valueStartIndex = 1
    )
trainingModel.populateModel()

alternativeModel = CustomModel.CustomSqlModel(
        database = str(database),
        table = "training_alternatives",
        tableStartIndex = 3,
        valueStartIndex = 1
    )
alternativeModel.populateModel()


exporter = Exporter.Exporter()
exporter.setDatabase(database)
exporter.setModel(trainingModel)
exporter.setName(configParser.readAttributes()["username"])

evaluator = GraphicalEvaluator.GraphicalEvaluator()

qapp = QtWidgets.QApplication(sys.argv)

app = mi.MainWindow(
        configParser = configParser,
        evaluator = evaluator,
        exporter = exporter,
        routineModel = trainingModel,
        alternativeModel = alternativeModel,
        database = database
    )

sys.exit(qapp.exec_())
