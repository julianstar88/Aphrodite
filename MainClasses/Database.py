# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:00 2020

@author: Julian

The Database-class  manages the data in a specific training_routine-file. It 
is possible to create, edit and delete training_routines, as well as add
data to the excersises within an training_routine.

A training_routine-file is a database-file created with SQLite3

Input:
    - no input
    
Attributes:
    - file_name: str 
    Name of the training_routine-file
    
    - path: str
    Path of the training_routine
    
    - cursor: cursor-object
    The cursor-object of the training_routine-file
    
Methods:
    - create()
    Create a new training_routine
    
    - delete()
    Delete a existing training_routine
    
    - edit()
    Edit data within a trainings_routine
    
    - getInformation()
    Load information about a exercise within a training_routine
    
    - registrateManagerData()
    Load necessary Data from the Manager-dict
    
Examples:
    - ToDo
"""
import sqlite3 as sql

class Database()

