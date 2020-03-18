# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:40 2020

@author: Julian
"""

import sys

from PyQt5 import QtWidgets

from CustomComponents import CustomBoxLayout, CustomScrollArea

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.widget = QtWidgets.QWidget()
        self.scrollArea = CustomScrollArea(self.widget)
        self.layout = CustomBoxLayout(QtWidgets.QBoxLayout.BottomToTop, self.widget)
        
        self.status = self.statusBar()
        
        self.setWindowTitle("Example")
        self.setGeometry(300,300,800,500)
        self.setCentralWidget(self.scrollArea)
        
        self.setStyleSheet("""
        
        QMainWindow {
            background-image: url(figures/nature/leaf.jpg);
            background-position: center center;
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