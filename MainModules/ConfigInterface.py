# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:02:27 2020

@author: Julian
"""
import pathlib2

class ConfigParser():

    def __init__(self):
        self._new_routine_directory = None
        self._last_opened_routine_directory = None
        self._export_routine_directory = None

    """getter"""
    @property
    def export_routine_directory(self):
        return self._export_routine_directory

    @property
    def last_opened_routine(self):
        return self._last_opened_routine_directory

    @property
    def new_routine_directory(self):
        return self._new_routine_directory

    """setter"""
    @export_routine_directory.setter
    def export_routine_directory(self, path):
        if not isinstance(path, str) and not isinstance(path, pathlib2.Path):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        path = pathlib2.Path(path)
        if not path.is_dir():
            raise ValueError(
                    "input <{input_name}> does not point to an existing directory".format(
                            input_name = str(path)
                        )
                )
        self._export_routine_directory = path

    @last_opened_routine.setter
    def last_opened_routine(self, path):
        if not isinstance(path, str) and not isinstance(path, pathlib2.Path):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        path = pathlib2.Path(path)
        if not path.is_file():
            raise ValueError(
                    "input <{input_name}> does not point to an existing file".format(
                            input_name = str(path)
                        )
                )
        self._last_opened_routine_directory = path

    @new_routine_directory.setter
    def new_routine_directory(self, path):
        if not isinstance(path, str) and not isinstance(path, pathlib2.Path):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(path),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        path = pathlib2.Path(path)
        if not path.is_dir():
            raise ValueError(
                    "input <{input_name}> does not point to an existing directory".format(
                            input_name = str(path)
                        )
                )
        self._new_routine_directory = path


    """config file manipulation"""
    def readConfigFile(self, file):
        if not isinstance(file, str) and not isinstance(file, pathlib2.Path):
            raise TypeError(
                    "input <{input_name}> does not match {type_name_1} or {type_name_2}".format(
                            input_name = str(file),
                            type_name_1 = pathlib2.Path,
                            type_name_2 = str
                        )
                )
        file = pathlib2.Path(file)
        if not file.is_file():
            raise ValueError(
                    "input <{input_name}> does not point to an existing file".format(
                            input_name = str(file)
                        )
                )

        with open(file, "r") as fh:
            rawData = fh.readlines()

        data = []
        for line in rawData:
            if "#" in line:
                del line
            else:
                line.strip("\n")
                processed = line.split(":")
                data.append(processed)
        print(data)


    def writeConfigFile(self, wdir):
        pass

if __name__ == "__main__":

    file = pathlib2.Path("files/config/config.txt")
    parentDir = pathlib2.Path().cwd().parent
    path = parentDir / file
    parser = ConfigParser()
    parser.readConfigFile(path)