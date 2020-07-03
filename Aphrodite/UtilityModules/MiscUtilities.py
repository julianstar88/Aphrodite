# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:50:27 2020

@author: Julian
"""
import re
import ast

class ModelInputValidation():

    def checkValue(self, value):
        """
        values have to adhere to the following pattern:

            "value1/value2/.../valueN"

            or

            "value"
        """

        match = re.split("/", value)
        for testVal in match:
            try:
                ast.literal_eval(testVal)
                return True
            except (ValueError, SyntaxError):
                return False

    def readValue(self, value):
        if self.checkValue(value):
            match = re.split("/", value)
            output = []
            for value in match:
                valid = eval(value)
                output.append(valid)
            return output
        else:
            return [None]

if __name__ == "__main__":
    testValues = ["5", "5/5/5", "sdfs", "sfdsdf/sdf/xdf", ""]
    validator = ModelInputValidation()

    for val in testValues:
        print(validator.readValue(val))
