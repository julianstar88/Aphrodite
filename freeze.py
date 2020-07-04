# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:19:01 2020

@author: Julian
"""
import PyInstaller.__main__
import sys
import pathlib2

sys.setrecursionlimit(5000)
iconPath = pathlib2.Path("files/icons")
iconName = pathlib2.Path("Aphrodite.ico")
PyInstaller.__main__.run([
        "--name=%s" % "Aphrodite",
        "--onedir",
        "--windowed",
        "Aphrodite.py"
    ])