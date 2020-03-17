# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:53:18 2020

@author: Julian
"""

import os
import sqlite3 as lite

class database():
    """
    Create a SQlite3 database file with the name 'name' and the columns
    'columns'. 
    
    Input parameter:
        -name: name of the generated database-file type: str
        -column_names: name and type of the colums in form of an tupel
            (("name", "type"), ("name", "type"),...)
            
    Output:
        - A db-file named 'name'
    """
    def __init__(self, name, column_names, table_name = None):
        self.__name = name
        self.__column_names = column_names
        
        if table_name == None:
            name, ext = os.path.splitext(self.__name)
            self.__table_name = name
        else:
            self.__table_name = table_name
        
        self.__con = None
        
        # establish connection to a database or create it if it not exists
        self.__establishConnection()
        
        # create table
        with self.__con:
    
            cur = self.__con.cursor()
            
            # comment if existing database-files should not be overwritten
            cur.execute("DROP TABLE IF EXISTS {name}".format(name = self.__table_name))
            
            value_string = ""
            for names in self.__column_names:
                value_string = value_string + "{} {}, ".format(names[0], names[1])
            
            value_string = value_string[:-2]
            cur.execute("CREATE TABLE {}({})".format(self.__table_name, value_string))
        
        # close connection after work is done
        self.__closeConnection()

    def addEntry(self, insert):
        
        # establish connection
        self.__establishConnection()
        
        # do work
        with self.__con:
            c = self.__con.cursor()
            values = '?, ' * len(insert)
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = self.__table_name, values = values)
            c.execute(sql_command, insert)
            
        # close connection
        self.__closeConnection()
            
    def addManyEntries(self, insert):
        
        # establish connection
        self.__establishConnection()
        
        with self.__con:
            c = self.__con.cursor()
            values = '?, ' * len(insert[0])
            values = values[:-2]
            sql_command = "INSERT INTO {name} VALUES({values})".format(
                name = self.__table_name, values = values)
            c.executemany(sql_command, insert)

        # close connection
        self.__closeConnection()

    def deleteEntry(self, row_id):
        
        # establish connection
        self.__establishConnection()
        
        with self.__con:
            c = self.__con.cursor()
            sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                name = self.__table_name, row_id = row_id)
            c.execute(sql_command)

        # close connection
        self.__closeConnection()
    
    def deleteManyEntries(self, row_id_list):

        # establish connection
        self.__establishConnection()

        with self.__con:
            c = self.__con.cursor()
            for idx in row_id_list:
                sql_command = "DELETE FROM {name} WHERE id = {row_id}".format(
                    name = self.__table_name, row_id = idx)
                c.execute(sql_command)
                
        # close connection
        self.__closeConnection()
            
    def deleteAllEntries(self):
        
        # establish connection
        self.__establishConnection()

        with self.__con:
            c = self.__con.cursor()
            sql_command = "DELETE FROM {name}".format(name = self.__table_name)
            c.execute(sql_command)
            
        # close connection
        self.__closeConnection()
    
    def getData(self):
        
        # establish connection
        self.__establishConnection()
        
        with self.__con:
            c = self.__con.cursor()
            sql_command = "SELECT * FROM {name}".format(name = self.__table_name)
            c.execute(sql_command)
            data = c.fetchall()
        
    
        # close connection
        self.__closeConnection()
        
        return data
        
    def __establishConnection(self):
        self.__con = lite.connect(self.__name)
    
    def __closeConnection(self):
        self.__con.close()

                
        
if __name__ == '__main__':
    
    # create databases
    # db = database("test_database_1.db", (("id", "INT"), ("name", "TEXT"), ("price", "INT")))
    # db2 = database("test_database_2.db", (("id", "INT"),("name", "TEXT"),("price", "INT")))
    # db3 = database("test_database_3.db", (("id", "INT"),("name", "TEXT"),("price", "INT")))
    # db4 = database("test_database_4.db", (("id", "INT"),("name", "TEXT"),("price", "INT")))
    # db5 = database("test_database_5.db", (("id", "INT"),("name", "TEXT"),("price", "INT")))
    
    db6 = database("test_database_6.db", (  
                                            ("id", "INT"),
                                            ("Exercise", "TEXT"), 
                                            ("Week_1", "TEXT"), 
                                            ("Week_2", "TEXT"), 
                                            ("Week_3", "TEXT"), 
                                            ("Week_4", "TEXT"), 
                                            ("Week_5", "TEXT"), 
                                            ("Week_6", "TEXT")
                                          )
                   )
    
    # create data for the databases
    l = [1, 'Saab', 15000]
    
    l2 = [
        [1, 'Audi', 52642],
        [2, 'Mercedes', 57127],
        [3, 'Skoda', 9000],
        [4, 'Bently', 350000],
        [5, 'Citroen', 21000],
        [6, 'Hummer', 41400],
        [7, 'Volkswagen', 21600]
        ]
    
    # training = [
    #     [1, "Bankdruecken", None, None, None, None, None, None],
    #     [2, "Klimmzuege", None, None, None, None, None, None],
    #     [3, "Kniebeugen", None, None, None, None, None, None],
    #     [4, "Bizeps SZ-Hantel", None, None, None, None, None, None],
    #     [5, "Trizeps Seilzug", None, None, None, None, None, None],
    #     [6, "Seitenheben KH", None, None, None, None, None, None]
    #     ]
    training = [
        [1, "Bankdruecken", "BD1", "BD2", "BD3", "BD4", "BD5", "BD6"],
        [2, "Klimmzuege", "KZ1", "KL2", "KL3", "KL4", "KL5", "KL6"],
        [3, "Kniebeugen", "KB1", "KB2", "KB3", "KB4", "KN5", "KB6"],
        [4, "Bizeps SZ-Hantel", "BZ1", "BZ2", "BZ3", "BZ4", "BZ5", "BZ6"],
        [5, "Trizeps Seilzug", "TZ1", "TZ2", "TZ3", "TZ4", "TZ5", "TZ6"],
        [6, "Seitenheben KH", "SH1", "SH2", "SH3", "SH4", "SH5", "SH6"]
        ]
    
    db6.addManyEntries(training)
    
    # # 1: add one entry to database1
    # db.addEntry(l)
    
    # # 2: add many entries to databse2
    # db2.addManyEntries(l2)
    
    # # 3: add many entries to databse3 and delete the first row
    # row_id = 1
    # db3.addManyEntries(l2)
    # db3.deleteEntry(row_id)
    
    # # 4: add many entries to database4 and delete the first three rows
    # row_id_list = [1, 2, 3]
    # db4.addManyEntries(l2)
    # db4.deleteManyEntries(row_id_list)
    
    # # 5: add many entries to database5 and delete all entries
    # db5.addManyEntries(l2)
    # db5.deleteAllEntries()
    
    # # 6: get Data from database2
    # data = db2.getData()
    
    
    