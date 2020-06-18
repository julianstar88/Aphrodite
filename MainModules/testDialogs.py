# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import sys
import MainModules.Database as db
import GuiModules.CustomGuiComponents as cc
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self.main = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main)
        self.setGeometry(100,100,800,500)
        self.setWindowTitle("Dialog Test")
        self.show()

        database = db.database("C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/test_files/test_database_2.db")

        self.dialog = cc.CustomEditAlternativesDialog(database, parent = self)
        if self.dialog.result():
            sys.exit()
        else:
            sys.exit()


qapp = QtWidgets.QApplication(sys.argv)

app = MainWindow()

sys.exit(qapp.exec_())