# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:40 2020

@author: Julian
"""

import sys

from PyQt5 import QtWidgets

from CustomComponents import CustomBoxLayout, CustomScrollArea, CustomWidget
from CustomModel import CustomSqlModel
from CustomTableView import CustomModelView

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.scrollArea = CustomScrollArea()
        self.widget = CustomWidget(self.scrollArea)
        self.layout = CustomBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self.widget)

        self.model = CustomSqlModel("database/test_database.db")

        headerLabels = [
                "Exercise",
                "Sets",
                "Repetitions",
                "Week 1",
                "Week 2",
                "Week 3",
                "Week 4",
                "Week 5",
                "Week 6"
            ]

        self.view = CustomModelView(self.model,
                                    headerLabels,
                                    fontSize = 15,
                                    fontWeight = "normal",
                                    parent = self.scrollArea
                                )

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
            background-color: rgba(255,255,255,0.2);
        }

        QHeaderView {
            background-color: rgba(51,153,255,0);
        }

        QHeaderView::section {
            background-color: rgba(51,153,255,0);
        }

        """)

        self.show()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())