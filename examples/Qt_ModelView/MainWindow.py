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

        self.model = CustomSqlModel(
                database = "database/test_database.db",
                table = "training_routine",
                tableStartIndex = 0,
            )
        self.model.populateModel()

        self.model2 = CustomSqlModel(
                database = "database/test_database.db",
                table = "training_alternatives",
                tableStartIndex = 3,
            )
        self.model2.populateModel()


        headerLabels = [
                "Exercise",
                "Sets",
                "Reps",
                "Warm Up",
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
                                    fontStyle = "normal",
                                    labelMode = "main",
                                    parent = self.scrollArea
                                )

        self.view2 = CustomModelView(self.model2,
                                    fontSize = 15,
                                    fontWeight = "normal",
                                    fontStyle = "normal",
                                    labelMode = "alternative",
                                    parent = self.scrollArea
                                )

        self.harmonizeColumnWidths(
                self.view,
                self.view2,
            )

        self.layout.addWidget(self.view)
        self.layout.addWidget(self.view2)

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

    def harmonizeColumnWidths(self, *args):
        newWidth = list()
        for table in args:
            header = table.horizontalHeader()
            width = list()
            for i in range(header.count()):
                width.append(header.sectionSize(i))
            width = max(width)
            newWidth.append(width)
        newWidth = max(newWidth)

        for table in args:
            header = table.horizontalHeader()
            table.setColumnWidth(0, newWidth)
            for i in range(header.count()):
                if i > 0:
                    table.resizeColumnToContents(i)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())