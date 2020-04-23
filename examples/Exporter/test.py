# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:58:19 2020

@author: Julian
"""

import pathlib2
import os.path

path = "C:/Users/Julian/Documents/Python/Projekte/Aphrodite/examples/Qt_ModelView/database/test_database.db"
pathObj = pathlib2.Path(1)
splitted = os.path.splitext(pathObj.name)

print(pathObj.parent)
print(splitted)
