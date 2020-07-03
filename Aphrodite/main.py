# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:59:00 2020

@author: Julian
"""
import sys
import pathlib2
import os
import GuiModules.MainInterface as mi
from MainModules import ConfigInterface
from PyQt5 import QtWidgets

def main():
    """settings"""
    configFileName = "config.txt"
    configPath = pathlib2.Path(
            "C:/Users/Julian/Documents/Python/Projekte/Aphrodite/Aphrodite/files/config"
        )
    currentPath = pathlib2.Path(__file__).cwd()
    defaultPath = pathlib2.Path(
            "C:/Users/Julian/Documents/Python/Projekte/Aphrodite/Aphrodite"
        )
    os.chdir(str(defaultPath))

    configParser = ConfigInterface.ConfigParser(configPath, configFileName)
    configFile = configParser.configDir() / configParser.configFileName()
    if not configFile.is_file():
        configParser.writeConfigFile()
    configParser.readConfigFile()

    """start app"""
    qapp = QtWidgets.QApplication(sys.argv)
    app = mi.MainWindow(configParser)
    try:
        sys.exit(qapp.exec_())
    except SystemExit:
        os.chdir(str(currentPath))

if __name__ == "__main__":
    main()
