# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import sys
from MainModules import Database
from GuiModules.CustomGuiComponents import CustomCreateNewRoutineDialog
from MainModules.ConfigInterface import ConfigParser
from PyQt5 import QtWidgets
import sqlite3

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self.main = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main)
        self.setGeometry(100,100,800,500)
        self.setWindowTitle("Dialog Test")
        self.show()

        configFileName = "config_testDialog.txt"
        configDir = "C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/config"
        parser = ConfigParser(configDir, configFileName)
        parser.writeConfigFile()

        database = Database.database("C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/test_files/test_database_2.db")

        self.dialog = CustomCreateNewRoutineDialog(
                database,
                parser,
                parent = self
            )
        if self.dialog.result():
            pass

qapp = QtWidgets.QApplication(sys.argv)

app = MainWindow()

sys.exit(qapp.exec_())