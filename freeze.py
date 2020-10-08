# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:19:01 2020

@author: Julian
"""
import PyInstaller.__main__
import sys
import pathlib

sys.setrecursionlimit(5000)
iconPath = pathlib.Path("files/icons")
iconName = pathlib.Path("Aphrodite.ico")
PyInstaller.__main__.run([
        "--name=%s" % "Aphrodite",
        "--onedir",
        "--windowed",
        "Aphrodite.py"
    ])