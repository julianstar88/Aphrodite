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
configFileName = "config.txt"
configDir = pathlib2.Path("files/config")
currentDir = pathlib2.Path(__file__).cwd()
configPath = currentDir / configDir

configParser = ConfigInterface.ConfigParser(configPath, configFileName)
configFile = configParser.configDir() / configParser.configFileName()
if not configFile.is_file():
    configParser.writeConfigFile()
configParser.readConfigFile()

"""start app"""
qapp = QtWidgets.QApplication(sys.argv)
app = mi.MainWindow(configParser)
sys.exit(qapp.exec_())
