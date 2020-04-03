# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:56:40 2020

@author: Julian
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5 import QtGui, QtWidgets

def createCanvas(mathText, color = "none", fontSize = 15, dpi = 100,
                  fontStyle = "normal", fontWeight = "normal",
                  fontColor = "black",
                  horizontalAlignment = "left",
                  verticalAlignment = "bottom"):

    fig = Figure()
    ax = fig.add_axes([0,0,1,1])
    fig.set_facecolor(color)
    fig.set_edgecolor(color)
    fig.set_dpi = dpi

    canvas = FigureCanvas(fig)
    renderer = canvas.get_renderer()

    ax.set_axis_off()
    t = ax.text(0, 0,
                mathText,
                color = fontColor,
                fontsize = fontSize,
                fontstyle = fontStyle,
                fontweight = fontWeight,
                horizontalalignment = horizontalAlignment,
                verticalalignment = verticalAlignment
                )

    text_bbox = t.get_window_extent(renderer)

    fheight = (text_bbox.height + 20) / dpi
    fwidth = (text_bbox.width + 5)/ dpi

    fig.set_size_inches(fwidth, fheight)

    # vertical centering of text in figure
    t.set_position((1.5/dpi, fheight/2))

    return canvas


def createQPixmap(canvas):
    buf, size = canvas.print_to_buffer()
    qimage = QtGui.QImage(buf, size[0], size[1], QtGui.QImage.Format_ARGB32)
    qpixmap = QtGui.QPixmap(qimage)
    return qpixmap

class GraphicalRoutineEditor(QtWidgets.QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = QtGui.QStandardItemModel(0, 10, self)
        self.__model.setHorizontalHeaderLabels(["Excercise",
                                              "Sets",
                                              "Reps",
                                              "Warm Up",
                                              "Week 1",
                                              "Week 2",
                                              "Week 3",
                                              "Week 4",
                                              "Week 5",
                                              "Week 6"])
        self.setModel(self.model())
        self.setColumnResizeMode()

    def setColumnResizeMode(self):
        for i in range(self.model().columnCount()):
            if i == 0:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def model(self):
        return self.__model




if __name__ == "__main__":

    canvas = createCanvas("test$^2$")