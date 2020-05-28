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
parentDir = pathlib2.Path().parent
configParser = ConfigInterface.ConfigParser()
configParser.readConfigFile(parentDir / configFile)

print(configParser.readAttributes()["current_routine"])

model = CustomModel.CustomSqlModel(
        database = configParser.readAttributes()["current_routine"],
        table = "training_routine",
        tableStartIndex = 1,
        valueStartIndex = 1
    )
model.populateModel()

database = pathlib2.Path(configParser.readAttributes()["current_routine"])

exporter = Exporter.Exporter()
exporter.setDatabase(database)

evaluator = GraphicalEvaluator.GraphicalEvaluator()
evaluator.setName(configParser.readAttributes()["username"])
evaluator.setDatabase(database)
evaluator.setModel(model)

qapp = QtWidgets.QApplication(sys.argv)

app = mi.MainWindow(
        configParser = configParser,
        evaluator = evaluator,
        exporter = exporter,
        model = model,
        database = database
    )

sys.exit(qapp.exec_())
