# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import inspect

def foo(one, two, three, test = None):
    sig = inspect.signature(foo)
    print(sig)

foo(1,2,3)