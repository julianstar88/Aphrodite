# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:56:40 2020

@author: Julian
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5 import QtGui
from PyQt5 import QtCore

def CreateCanvas(mathText, color = "none", fontSize = 15, dpi = 100,
                  fontStyle = "normal", fontWeight = "normal",
                  fontColor = "black",
                  horizontalAlignment = "left",
                  verticalAlignment = "bottom",
                  usetex = False):

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
                verticalalignment = verticalAlignment,
                usetex = usetex
                )

    text_bbox = t.get_window_extent(renderer)

    # fheight = (text_bbox.height / dpi) + (ax.get_position().height - (text_bbox.height / dpi))
    fheight = (text_bbox.height / dpi) + ax.get_position().height*0.5
    fwidth = (text_bbox.width / dpi) + ax.get_position().width

    # fheight = (text_bbox.height + 20) / dpi
    # fwidth = (text_bbox.width + 5)/ dpi

    fig.set_size_inches(fwidth, fheight)

    # vertical centering of text in figure
    t.set_position((1.5/dpi, fheight/1.5))
    # t.set_position((1.5/dpi, fheight/2))

    return canvas

def CreateQPixmap(canvas):
    buf, size = canvas.print_to_buffer()
    qimage = QtGui.QImage(buf, size[0], size[1], QtGui.QImage.Format_ARGB32)
    qpixmap = QtGui.QPixmap(qimage)
    return qpixmap

if __name__ == "__main__":
    pass