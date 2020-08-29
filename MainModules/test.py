# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""

import datetime

date = datetime.date.today()

strDate = date.strftime("%y%m%d")

name = "Training-{date}".format(
     date = strDate
    )

print(name)