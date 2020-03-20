# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:20:29 2020

@author: Julian
"""

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

mathText = "test$^2$"
color = "none" #(0.6,0.6,0.6,1)
fontSize = 30
fontStyle = "normal"
fontWeight = "normal"
horizontalAlignment = "left"
verticalAlignment = "bottom"
dpi = 100

fig, ax = plt.subplots()
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

fheight = text_bbox.height / dpi
fwidth = text_bbox.width / dpi

fig.set_size_inches(fwidth, fheight)


