# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:20:29 2020

@author: Julian
"""

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

color = (0.6,0.6,0.6,1)
fontSize = 30
fontStyle = "normal"
fontWeight = "normal"

fig, ax = plt.subplots()
fig.set_facecolor(color)
fig.set_edgecolor(color)

canvas = FigureCanvas(fig)
renderer = canvas.get_renderer()

ax.set_axis_off()
t = ax.text(0,0,"test", 
            fontsize = fontSize, 
            fontstyle = fontStyle,
            fontweight = fontWeight
            )

text_bbox = t.get_window_extent(renderer)
