# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import sys
import GuiModules.MainInterface as mi
from PyQt5 import QtWidgets

qapp = QtWidgets.QApplication(sys.argv)

app = mi.MainWindow()

sys.exit(qapp.exec_())


