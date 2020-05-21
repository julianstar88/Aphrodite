# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:58:37 2020

@author: Julian
"""

import sys
import GuiModules.CustomGuiComponents as cc
import UtilityModules.GraphicUtilityModules as gum
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Aphrodite")
        self.mainWidget = cc.CustomWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        labels = ["test1", "test2", "test3"]
        values = ["testText$^1$", "testText$^2$", "testText$^3$"]
        panel1 = Panel(labels, values)

        labels = ["test4", "test5", "test6"]
        values = ["testText$^4$", "testText$^5$", "testText$^6$"]
        panel2 = Panel(labels, values)

        tabpanel = QtWidgets.QTabWidget(self)

        self.mainLayout.addWidget(panel1,0,0)
        self.mainLayout.addWidget(panel2,1,0)

        self.show()

class Panel(cc.CustomWidget):

    def __init__(self, labels, values,  *args):
        super().__init__(*args)
        self._labels = None
        self._values = None

        self.setLabels(labels)
        self.setValues(values)

        self.createPanel()

        self.setStyleSheet(
                """
                CustomWidget {background-color: rgba(255,255,255,100%)}
                """
            )

    def createPanel(self):
        layout = QtWidgets.QGridLayout()

        for i, val in enumerate(self.labels()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = 15
                )
            pixmap = gum.CreateQPixmap(canvas)
            label = cc.CustomLabel(pixmap)
            layout.addWidget(
                    label, i, 0
                )

        for i, val in enumerate(self.values()):
            canvas = gum.CreateCanvas(
                    val,
                    fontSize = 15,
                    horizontalAlignment = "left",
                    dpi = 100
                )
            pixmap = gum.CreateQPixmap(canvas)
            label = cc.CustomLabel(pixmap)
            layout.addWidget(
                    label, i, 1
                )

        self.setLayout(layout)
        return self

    def labels(self):
        return self._labels

    def setLabels(self, labels):
        if not isinstance(labels, list):
            raise TypeError(
                    "Panel.setLabels: input <{input_name}> does not match {type_name}".format(
                            input_name = str(labels),
                            type_name = list
                        )
                )
        self._labels = labels

    def setValues(self, values):
        if not isinstance(values, list):
            raise TypeError(
                    "Panel.setValues: input <{input_name}> does not match {type_name}".format(
                            input_name = str(values),
                            type_name = list
                        )
                )
        self._values = values

    def values(self):
        return self._values


class RoutineTab(cc.CustomWidget):

    def __init__(self, *args):
        super().__init__(*args)

class EvaluatorTab(cc.CustomWidget):

    def __init__(self, *args):
        super().__init__(*args)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = MainWindow()

    sys.exit(qapp.exec_())