# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:54:54 2020

@author: Julian
"""


from PyQt5 import QtWidgets, QtGui, QtCore
from CustomHeaderview import CustomHeader
from HelperBaseClasses import createCanvas, createQPixmap

class CustomModelView(QtWidgets.QTableView):

    def __init__(self, model, headerLabels, fontSize = 15, fontWeight = "normal"):
        super().__init__()
        self.setModel(model)
        self.setHorizontalHeader(CustomHeader(self))
        self.verticalHeader().hide()

        self.__setHorizontalHeaderLabels(headerLabels, fontSize, fontWeight)

    def __setColumnResizeMode(self):
        pass

    def __setHorizontalHeaderLabels(self, headerLabels, fontSize, fontWeight):
        qpixmaps = list()

        for i, label in enumerate(headerLabels):
            canvas = createCanvas(label,
                                  horizontalAlignment = "left",
                                  verticalAlignment = "bottom")
            pixmap = createQPixmap(canvas)
            qpixmaps.append(pixmap)
            self.setColumnWidth(i, pixmap.size().width())
        self.horizontalHeader().qpixmaps = qpixmaps


