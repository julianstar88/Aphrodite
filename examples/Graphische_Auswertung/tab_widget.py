# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 21:52:00 2020

@author: Julian
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('tab widget test')
        
        self.tab_widget = Example()
        self.setCentralWidget(self.tab_widget)
        
        self.show()
        

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tabs.addTab(tab1(), "Tab1")
        self.tabs.addTab(tab2(), "Tab2")
        self.tabs.addTab(tab3(), "Tab3")
        self.tabs.addTab(tab4(), "Tab4")
        
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class tab1(QWidget):
    
    def __init__(self):
        super().__init__()
        
class tab2(QWidget):
    
    def __init__(self):
        super().__init__()
        
class tab3(QWidget):
    
    def __init__(self):
        super().__init__()
        
class tab4(QWidget):
    
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = App()
    
    sys.exit(app.exec_())