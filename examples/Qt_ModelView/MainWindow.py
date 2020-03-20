# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:40 2020

@author: Julian
"""

import sys

from PyQt5 import QtWidgets

from CustomComponents import CustomBoxLayout, CustomScrollArea
from CustomModel import CustomSqlModel
from CustomTableView import CustomModelView

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.widget = QtWidgets.QWidget()
        self.scrollArea = CustomScrollArea(self.widget)
        self.layout = CustomBoxLayout(QtWidgets.QBoxLayout.BottomToTop, self.widget)

        self.model = CustomSqlModel("database/test_database.db")

        headerLabels = [
                "Exercise",
                "Sets",
                "Repetitions",
                "Week$_1$",
                "Week$_2$",
                "Week$_3$",
                "Week$_4$",
                "Week$_5$",
                "Week$_6$"
            ]

        self.view = CustomModelView(self.model,
                                    headerLabels,
                                    fontSize = 15,
                                    fontWeight = "normal")

        self.layout.addWidget(self.view)

        self.status = self.statusBar()

        self.setWindowTitle("Example")
        self.setGeometry(300,300,800,500)
        self.setCentralWidget(self.view)

        self.setStyleSheet("""

        QMainWindow {
            background-image: url(figures/nature/leaf.jpg);
            background-position: bottom right;
            background-origin: content;
        }

        QTableView {
            background-color: rgba(160,160,160,0.3);
        }

        QHeaderView {}

        QHeaderView::section {}

        """)

        self.show()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())