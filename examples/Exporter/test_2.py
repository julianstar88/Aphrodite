# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:58:19 2020

@author: Julian
"""

import datetime

date1 = datetime.date(2020, 4, 16)
dt = datetime.timedelta(days = 42)
date2 = date1 + dt

print(date1.strftime("%d.%m.%Y"))
print(date2.strftime("%d.%m.%Y"))