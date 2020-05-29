# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import re
import pathlib2

value = "C:/Users/Julian/Documents/Python/Projekte/Aphrodite/files/config/config.txt"
key = "test_path"
string = "{}:{}".format(key, value)
pattern1 = "(?P<key>\w*):(?P<value>([\w\W]*):?([\\/]?[\w\W])*)"
pattern2 = "(?P<key>\w*):(?P<value>[\w\W]*:?[\\/]?[\w\W]*)"

stripped = string.strip("\n")
match = re.search(pattern2, string)

print(match)
print("key:", match.group("key"))
print("value:", match.group("value"))

t = int("2")

