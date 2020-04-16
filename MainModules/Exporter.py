# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:30:14 2020

@author: Julian
"""
import openpyxl
import datetime
import unittest
from openpyxl.styles import Alignment, Border, Color, Font, PatternFill, Side
from Utility_Function_Library.converter import ColorConverter


class Exporter():

    def __init__(self,
                 name = None,
                 routineName = None,
                 trainingPeriode = [None, None],
                 trainingMode = None):

        self.__name = name
        self.__routineName = routineName
        self.__trainingPeriode = trainingPeriode
        self.__trainingMode = trainingMode

    def name(self):
        return self.__name

    def routineName(self):
        return self.__routineName

    def trainingPeriode(self):
        return self.__trainingPeriode

    def trainingMode(self):
        return self.__trainingMode

    def setName(self, name):
        if not type(name) == str:
            raise TypeError(
                "input argument {name} does not match {type_name}".format(
                        name = name,
                        type_name = type("str")
                    )
                )
        elif len(name) == 0:
            raise ValueError("empty input for the attribute 'name'")
        else:
            self.__name = name

    def setRoutineName(self, routineName):
        if not type(routineName) == str:
            raise TypeError(
                "input argument {name} does not match {type_name}".format(
                        name = routineName,
                        type_name = type("str")
                    )
                )
        elif len(routineName) == 0:
            raise ValueError("empty input for the attribute 'routineName'")
        else:
            self.__routineName = routineName

    def setTrainingPeriode(self, startYear, startMonth, startDay):
        if not type(startYear) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {tpye_name}""".format(
                            name = startYear,
                            type_name = type(123)
                        )
                )
        if not type(startMonth) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {tpye_name}""".format(
                            name = startMonth,
                            type_name = type(123)
                        )
                )
        if not type(startDay) == int:
            raise TypeError(
                    """input argument '{name}' for <startYear>
                    does not match {tpye_name}""".format(
                            name = startDay,
                            type_name = type(123)
                        )
                )
        startDate = datetime.date(startYear, startMonth, startDay)
        endDate = startDate + datetime.timedelta(days = 42)
        self.__trainingPeriode = (startDate, endDate)
