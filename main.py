# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:59:00 2020

@author: Julian
"""
import sys
import pathlib2
import GuiModules.MainInterface as mi
from MainModules import ConfigInterface, Database, Exporter, GraphicalEvaluator
from UtilityModules import CustomModel
from PyQt5 import QtWidgets

"""settings"""
configFile = pathlib2.Path("files/config/config.txt")
parentDir = pathlib2.Path().cwd()
configParser = ConfigInterface.ConfigParser(parentDir / configFile)
configParser.readConfigFile()

databaseFile = pathlib2.Path(configParser.readAttributes()["last_opened_routine"])

"""critical error, if config-file is invalid"""
if not databaseFile.is_file():
    raise RuntimeError(
            "no config-file found"
        )

"""neccessary objects for aphrodite"""
databaseObject = Database.database(databaseFile)

trainingModel = CustomModel.CustomSqlModel(
        database = str(databaseFile),
        table = "training_routine",
        tableStartIndex = 0,
        valueStartIndex = 1
    )
trainingModel.populateModel()

alternativeModel = CustomModel.CustomSqlModel(
        database = str(databaseFile),
        table = "training_alternatives",
        tableStartIndex = 3,
        valueStartIndex = 1
    )
alternativeModel.populateModel()

exporterData = databaseObject.data("general_information")
exporter = Exporter.Exporter()
exporter.setDatabase(databaseFile)
exporter.setModel(trainingModel)
exporter.setName(exporterData[0][0])

evaluator = GraphicalEvaluator.GraphicalEvaluator()

"""start app"""
qapp = QtWidgets.QApplication(sys.argv)
app = mi.MainWindow(
        configParser = configParser,
        evaluator = evaluator,
        exporter = exporter,
        routineModel = trainingModel,
        alternativeModel = alternativeModel,
        database = databaseObject
    )
sys.exit(qapp.exec_())
