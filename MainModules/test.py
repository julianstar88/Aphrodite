"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
t = {
         "one":1,
         "two":2,
         "three":3
     }
t2 = {
          "one": 4,
          "two": 5,
          "three": 6
      }

for key in t2:
    if key in t:
        t[key] = t2[key]