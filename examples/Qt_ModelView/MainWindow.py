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

        self.widget = CustomWidget()
        self.scrollArea = CustomScrollArea(self.widget)
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

        self.view2 = CustomModelView(self.model,
                                    headerLabels,
                                    fontSize = 15,
                                    fontWeight = "normal",
                                    parent = self.scrollArea
                                )

        self.view3 = CustomModelView(self.model,
                                    headerLabels,
                                    fontSize = 15,
                                    fontWeight = "normal",
                                    parent = self.scrollArea
                                )

        self.view4 = CustomModelView(self.model,
                                    headerLabels,
                                    fontSize = 15,
                                    fontWeight = "normal",
                                    parent = self.scrollArea
                                )

        self.layout.addWidget(self.view)
        self.layout.addWidget(self.view2)
        self.layout.addWidget(self.view3)
        self.layout.addWidget(self.view4)

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

        QTableView {
            background-color: rgba(255,255,255,40%);
            gridline-color: gray;
        }

        QHeaderView {
            background-color: rgba(51,153,255,0%);
        }

        QHeaderView::section {
            background-color: rgba(51,153,255,0%);
        }

        QScrollArea {
            background-color: rgba(255,255,255,0%);
        }

        """)

        self.show()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())