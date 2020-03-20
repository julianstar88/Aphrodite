# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:56:40 2020

@author: Julian
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5 import QtCore, QtGui

def createCanvas(mathText, color = "none", fontSize = 15, dpi = 100,
                  fontStyle = "normal", fontWeight = "normal",
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
    t = ax.text(0,0,mathText,
                fontsize = fontSize,
                fontstyle = fontStyle,
                fontweight = fontWeight,
                horizontalalignment = horizontalAlignment,
                verticalalignment = verticalAlignment
                )

    text_bbox = t.get_window_extent(renderer)

    fheight = (text_bbox.height + 20) / dpi
    fwidth = (text_bbox.width + 20)/ dpi

    fig.set_size_inches(fwidth, fheight)

    return canvas


def createQPixmap(canvas):
    buf, size = canvas.print_to_buffer()
    qimage = QtGui.QImage(buf, size[0], size[1], QtGui.QImage.Format_ARGB32)
    qpixmap = QtGui.QPixmap(qimage)
    return qpixmap

class evaluateClickEvent():
    pass


if __name__ == "__main__":

    canvas = createCanvas("test$^2$")