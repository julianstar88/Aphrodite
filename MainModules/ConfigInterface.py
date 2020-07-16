# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:02:27 2020

@author: Julian
"""
import pathlib2
import re
import copy

class ConfigParser():

    knownConfigKeys = (
        "new_routine_directory",
        "last_opened_routine",
        "last_closed_routine",
        "export_routine_directory"
    )

    def __init__(self, configDir = None, configFileName = None):
        self._configFileName = None
        self._configDir = None

        if configDir is not None:
            self.setConfigDir(configDir)

        if configDir is not None:
            self.setConfigFileName(configFileName)

    def addAttributes(self, attributes, values):
        if not isinstance(attributes, list) and not isinstance(attributes, tuple):
            raise TypeError(
                    "input <{input_name}> for 'attributes' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(attributes),
                            type_name_1 = list,
                            type_name_2 = tuple
                        )
                )
        if not isinstance(values, list) and not isinstance(values, tuple):
            raise TypeError(
                    "input <{input_name}> for 'values' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(values),
                            type_name_1 = list,
                            type_name_2 = tuple
                        )
                )
        for (key, value) in zip(attributes, values):
            self.__dict__[key] = value

    def configDir(self):
        return self._configDir

    def configFileName(self):
        return self._configFileName

    def readAttributes(self):
        attr = copy.deepcopy(self.__dict__)
        keys = list(attr.keys())
        for key in keys:
            match = re.search("^_\w+", key)
            if match:
                del attr[key]
        return attr


    def readConfigFile(self, file = None):
        if file is not None:
            self.setConfigDir(file)

        path = self.configDir() / self.configFileName()
        if not path.is_file():
            return False
        with open(path, "r") as fh:
            rawData = fh.readlines()

        data = list()
        for line in rawData:
            stripped = line.strip("\n")
            pattern = "(?P<key>\w*):(?P<value>[\w\W]*:?[\\/]?[\w\W]*)"
            match = re.search(pattern, stripped)
            data.append([match.group("key"), match.group("value")])
        keys = [key[0] for key in data]
        vals = [val[1] for val in data]
        self.addAttributes(keys, vals)

        return True

    def setConfigDir(self, wdir):
        if not isinstance(wdir, pathlib2.Path) and not isinstance(wdir, str):
            raise TypeError(
                    "input <{input_name}> for 'setConfigDir' does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(wdir),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        path = pathlib2.Path(wdir)
        if (not path.is_dir()) and (not path.is_file()):
            raise ValueError(
                    "input <{input_name}> does not point to an existing directory or file".format(
                            input_name = str(path)
                        )
                )
        if path.is_dir():
            self._configDir = path
        if path.is_file():
            self._configDir = path.parent
            self.setConfigFileName(path.name)

    def setConfigFileName(self, fileName):
        # if not isinstance(file, pathlib2.Path) and not isinstance(file, str):
        #     raise TypeError(
        #             "input <{input_name}> for 'setConfigFile' does not match {type_name_1} or {type_name_2}".format(
        #                     input_name = str(file),
        #                     type_name_1 = pathlib2.Path,
        #                     type_name_2 = str
        #                 )
        #         )
        # path = pathlib2.Path(file)
        # if not path.is_file():
        #     raise ValueError(
        #             "input <{input_name}> does not point to an existing file".format(
        #                     input_name = str(path)
        #                 )
        #         )
        # self.setConfigDir(path.parent)
        # self._configFile = path.name
        if not isinstance(fileName, str):
            raise TypeError(
                    "input <{input_name} does not match {type_name}>".format(
                            input_name = str(fileName),
                            type_name = str
                        )
                )
        self._configFileName = fileName

    def writeConfigFile(self, fileName = None, wdir = None, mode = "w"):
        if fileName is not None:
            self.setConfigFileName(fileName)

        if wdir is not None:
            self.setConfigDir(wdir)

        if (not isinstance(self.configFileName(), str)):
            raise TypeError(
                    "the value <{value_name}> for 'configFileName' is not valid".format(
                            value_name = str(self.configFileName())
                        )
                )

        if (not isinstance(self.configDir(), pathlib2.Path)):
            raise TypeError(
                    "the value <{value_name}> for 'configDir' is not valid".format(
                            value_name = str(self.configDir())
                        )
                )

        if not isinstance(mode, str):
            raise TypeError(
                    "input <{input_name}> for 'mode' does not match {type_name}".format(
                            input_name = str(mode)
                        )
                )
        if not mode in ["w", "a"]:
            raise ValueError(
                    "input <{input_name}> for 'mode' does not match 'w' or 'a'".format(
                            input_name = str(mode)
                        )
                )
        with open(self.configDir() / self.configFileName(), mode) as fh:
            keys = list(self.readAttributes().keys())
            if not keys:
                configKeys = type(self).knownConfigKeys
                configValues = [""]*len(configKeys)
                self.addAttributes(configKeys, configValues)
            keys = list(self.readAttributes().keys())
            for key in keys:
                line = "{key}:{val}\n".format(
                        key = key,
                        val = self.readAttributes()[key]
                    )
                fh.write(line)

if __name__ == "__main__":

    file = pathlib2.Path("files/config/config.txt")
    parentDir = pathlib2.Path().cwd().parent
    path = parentDir / file
    parser = ConfigParser()
    parser.readConfigFile(path)