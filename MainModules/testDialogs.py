# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import sys
from MainModules import Database
from GuiModules.CustomGuiComponents import CustomEditRoutineDialog
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

        # database = Database.database("C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/test_files/test_database_2.db")
        database = Database.database("C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/test_files/empty_database.db")

        self.dialog = CustomEditRoutineDialog(
                database,
                parent = self,
            )
        if self.dialog.result():
            print(self.dialog.toCommit()["training_routine"])
            for key in self.dialog.toCommit().keys():
                self.dialog.database().deleteAllEntries(key)
                self.dialog.database().addManyEntries(key, self.dialog.toCommit()[key])
        else:
            sys.exit()


qapp = QtWidgets.QApplication(sys.argv)

app = MainWindow()

sys.exit(qapp.exec_())