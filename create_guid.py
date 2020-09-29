# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 23:27:04 2020

@author: Julian
"""
from comtypes.GUID import GUID

def return_guid():
    new = GUID.create_new()
    return new

if __name__ == "__main__":
    new = return_guid()
    print(new)