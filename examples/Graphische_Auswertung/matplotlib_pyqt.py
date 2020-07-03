# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:35:43 2020

@author: Julian

Um eine Matplotlib-Grafik in eine PyQt5-App zu integrieren ist das Modul 
"FigureCanvas" von "matplotlib.backends.backend_qt5agg" notwendig.

Folgende Schritte sind abzuarbeiten:
    
    1. Erzeugen eines QWidgets
    2. Erzeugen eines Layouts (QWidget als Perant)
    3. Erzeugen einer Figure und eines Axes
    4. Erzeugen der FigureCanvas-Instanz (mit der in 3. erzeugten figure als Parent)
    5. Hinzufügen des FigureCanvas zum Layout aus 2.
    
IMPORTANT:
    load all required PyQt5 modules before matplotlib libraries. Otherwise the 
    script doesn´t work in an external system terminal

"""

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

import numpy as np
# from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1: create a QWidget and set it to the central widget of MainWindow
        self.main = QWidget()
        self.setWindowTitle("Matplotlib integration in PyQt5")
        self.setCentralWidget(self.main)
        
        # 2: create a layout with the QWidget as its parent
        layout = QVBoxLayout(self.main)
        
        # 2: create an axes and a figure
        ## self.fig is an instance of matplotlib.figure.Figure
        ## self.ax is an instance of matplotlib.axes.Axes 
        self.fig, self.ax = plt.subplots()
        
        ## costumize self.ax
        
        ### create xticks in the range of 0 to 2*pi
        xticks = [xtick for xtick in np.linspace(0, 4, 5)*0.5*np.pi]
        self.ax.set_xticks(xticks)
        
        ### create lables for the xticks
        xticklabels = ["$\\dfrac{0}{2}$", "$\\dfrac{1}{2}$", "$\\dfrac{2}{2}$", "$\\dfrac{3}{2}$", "$\\dfrac{4}{2}$"]
        self.ax.set_xticklabels(xticklabels)
        
        ### create xlabels and ylabels
        self.ax.set_ylabel("a.u.")
        self.ax.set_xlabel("radian / $\pi$")
        
        # 3: create canvas and add it to the layout
        canvas = FigureCanvas(self.fig)
        layout.addWidget(canvas)
        
        # 4: create data and plot it
        x = np.linspace(0,2*np.pi)
        y = np.sin(x)
        self.ax.plot(x,y)

        # use tight layout for the figure to ensure the correct alignment
        # for all components of the figure
        self.fig.tight_layout()
        
        # show application
        self.show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main = MainWindow()
    
    sys.exit(app.exec_())
    