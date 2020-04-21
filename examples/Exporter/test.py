# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:58:19 2020

@author: Julian
"""

import examples.SQLite3_Database.Database as db

db = db.database()
# db.createTable(
#         "test", "testTable",
#         (
#             ("col1", "TEXT"),
#             ("col2", "TEXT"),
#             ("col3", "TEXT")
#         )
#     )
db.deleteAllEntries("test.db", "testTable")