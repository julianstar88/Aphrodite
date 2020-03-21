# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:20:29 2020

@author: Julian
"""

from CustomComponents import CustomModelItem

if __name__ == "__main__":
    l = list()
    t = CustomModelItem("test")
    t2 = CustomModelItem("test2")
    l.append(t)
    l.append(t2)

    print(type(l[0]))
