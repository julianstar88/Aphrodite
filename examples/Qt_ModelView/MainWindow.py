# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:40 2020

@author: Julian
"""

import sys

from PyQt5 import QtWidgets

from CustomComponents import CustomBoxLayout, CustomScrollArea
from CustomModel import CustomSqlModel

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.widget = QtWidgets.QWidget()
        self.scrollArea = CustomScrollArea(self.widget)
        self.layout = CustomBoxLayout(QtWidgets.QBoxLayout.BottomToTop, self.widget)
        
        self.model = CustomSqlModel("database/test_database.db")
        
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        self.layout.addWidget(self.view)
        
        self.status = self.statusBar()
        
        self.setWindowTitle("Example")
        self.setGeometry(300,300,800,500)
        self.setCentralWidget(self.scrollArea)
        
        self.setStyleSheet("""
        
        QMainWindow {
            background-image: url(figures/nature/leaf.jpg);
            background-position: bottom right;
            background-origin: content;
        }
        
        QScrollArea {
            background-color: rgba(255,255,255,0);
        }
        
        QTableView {}
        
        QHeaderView {}
        
        QHeaderView::section {}
        
        """)
        
        self.show()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    
    app = MainWindow()
    
    sys.exit(qapp.exec_())