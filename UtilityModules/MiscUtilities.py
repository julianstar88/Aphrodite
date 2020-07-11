# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:50:27 2020

@author: Julian
"""
import re
import ast
import sys
import os
import pathlib2

class ModelInputValidation():

    def checkValue(self, value):
        """
        values have to adhere to the following pattern:

            "value1/value2/.../valueN"

            or

            "value"
        """

        match = re.split("/", value)
        if not match:
            return False

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

class EnvironmentBase():

    def __init__(self, path = None, fileName = "default_file.txt"):
        self._path = None
        self._fileName = None

        if path:
            self.setPath(path)
        else:
            self.setPath(pathlib2.Path(__file__).cwd())
        self.setFileName(fileName)

    def file(self):
        try:
            file = self.path() / self.fileName()
        except TypeError:
            return None

        return file

    def fileName(self):
        return self._fileName

    def path(self):
        return self._path

    def setFileName(self, name):
        if not isinstance(name, str):
            return False

        self._fileName = name
        return True

    def setPath(self, path):
        path = pathlib2.Path(path)
        if path.is_dir():
            self._path = path
            return True
        elif path.is_file():
            self._path = path.parent
            self.setFileName(path.name)
            return True
        else:
            return False

class EnvironmentComparer(EnvironmentBase):

    def __init__(self, path = None, diffFileName = "diffs.txt"):
        super().__init__(path, diffFileName)
        self._diffs = list()
        self._commonLines = list()

    def compareEnvs(self, env1, env2, withOutput = False):
        linesEnv1, linesEnv2 = self.openEnvs(env1, env2)
        commonKeys = self.commonKeys(env1, env2, withOutput)

        env1Dict = dict()
        for line in linesEnv1:
            env1Dict[line[0]] = line[1]

        env2Dict = dict()
        for line in linesEnv2:
            env2Dict[line[0]] = line[1]

        for i, key in enumerate(commonKeys):
            env1Value = env1Dict[key]
            env2Value = env2Dict[key]
            envValues = [env1Value, env2Value]
            lenEnvs = [len(env) for env in envValues]
            maxEnv = lenEnvs.index(max(lenEnvs))
            minEnv = lenEnvs.index(min(lenEnvs))
            diffDict = {"env1": list(), "env2": list()}

            for n in range(lenEnvs[minEnv]):
                if env1Value[n] != env2Value[n]:
                    diffDict["env1"].append({"diff":env1Value[n]})
                    diffDict["env2"].append({"diff":env2Value[n]})
            for n in range(lenEnvs[minEnv], lenEnvs[maxEnv]):
                envName = "env" + str(maxEnv + 1)
                if len(set(lenEnvs)) > 1:
                    diffDict[envName].append({"+": envValues[maxEnv][n]})

            diffs = [i + 1, key, diffDict["env1"], diffDict["env2"]]
            self._diffs.append(diffs)

        if withOutput:
            print("difference in environment variables:")
            print("-"*36)
            for diff in self._diffs:
                print(diff)


    def commonKeys(self, env1, env2, withOutput = False):

        linesEnv1, linesEnv2 = self.openEnvs(env1, env2)
        keysEnv1 = [lines[0] for lines in linesEnv1]
        keysEnv2 = [lines[0] for lines in linesEnv2]
        if len(linesEnv1) > len(linesEnv2):
            if withOutput:
                print("common environment variables:")
                print("-"*30)
            for line in linesEnv1:
                if withOutput:
                    result = line[0] in keysEnv2
                    print("{}:".format(line[0]) + str(result))
            commonKeys = [line[0] for line in linesEnv1 if line[0] in keysEnv2]
            print("")
            print("")
        else:
            if withOutput:
                print("common environment variables:")
                print("-"*30)
            for line in linesEnv2:
                if withOutput:
                    result = line[0] in keysEnv1
                    print("{}:".format(line[0]) + str(result))
            commonKeys = [line[0] for line in linesEnv2 if line[0] in keysEnv1]
            print("")
            print("")

        self._commonKeys = commonKeys
        return commonKeys

    def diff(self):
        """
        diff represents the differences between the variables in two environmants.
        the list looks like the following example:
            diff = [
                    [linNo., var, file1, file2]
                    ...
                ]
        the elements have the following meaning:
            lineNo: linenumber, where the difference occurs
            var: environment variables which are different in the compared environments
            file1, file2: represent the kind of differences which has been detected
            diff: actually the difference of var in compared environments

        the kind of differences written to file1/file2 could be:
            0: remarks differences between entries in file1 and file2
            +: denotes, that this entry is only in file1 or file2

        Returns
        -------
        list
            list of differences of environments env1 and env1.

        """
        return self._diff

    def diff2File(self):
        header = "#line \t Environment Variable \t Environment 1 \t Environment 2\n"
        ruler = "-"*63

        with open(self.file(), "w") as file:
            file.write(header)
            file.write(ruler)

    def openEnvs(self, env1, env2):
        with open(env1, "r") as file:
            linesEnv1 = file.readlines()

        with open(env2, "r") as file:
            linesEnv2 = file.readlines()

        for i, line in enumerate(linesEnv1):
            items = line.split(":: ")
            items[1] = items[1].strip("\n")
            items[1] = items[1].split(";")
            items[1] = [item.strip(" ") for item in items[1]]
            linesEnv1[i] = items

        for i, line in enumerate(linesEnv2):
            items = line.split(":: ")
            items[1] = items[1].strip("\n")
            items[1] = items[1].split(";")
            items[1] = [item.strip(" ") for item in items[1]]
            linesEnv2[i] = items

        return linesEnv1, linesEnv2

class EnvironmentFreezer(EnvironmentBase):

    def __init__(self, path = None, fileName = "file1.txt"):
        super().__init__(path, fileName)

    def env2File(self, path = None, fileName = None, withOutput = True):
        if withOutput:
            print(self.fileName())
            print(self.path())
            print(self.file())
            print("")
            print("freezing Environment --> {}".format(self.fileName()))

        if path:
            self.setPath(path)

        if fileName:
            self.setFileName(fileName)

        with open(self.file(), "w") as file:
            for item in os.environ:
                string = "{}:: {}\n".format(
                        item,
                        os.environ[item]
                    )
                file.write(string)
        if withOutput:
            print("Done")
            print("")

    def file2Env(self, path = None, fileName = None, withOutput = True):
        if withOutput:
            print(self.fileName())
            print(self.path())
            print(self.file())
            print("")
            print("solving Environment <-- {}".format(self.fileName()))

        if path:
            self.setPath(path)

        if fileName:
            self.setFileName(fileName)

        with open(self.file(), "r") as file:
            lines = file.readlines()

        items = list()
        for line in lines:
            item = line.split("::")
            items.append(item)

        for item in items:
            os.environ[item[0]] = item[1].strip(" \n")
            # try:
            #     os.environ[item[0]] = item[1]
            # except:
            #     if withOutput:
            #         print("Done with errors:")
            #         print("")
        if withOutput:
            print("Done")
            print("")

    def sysPath2File(self, path = None, fileName = None):
        with open(self.file(), "w") as file:
            for line in sys.path:
                file.write(line + "\n")

if __name__ == "__main__":
    wdir = pathlib2.Path(__file__).cwd().parent
    fileName = "env_python.txt"
    freezer = EnvironmentFreezer(
            path = wdir,
            fileName = fileName
        )
    comparer = EnvironmentComparer(
            path = wdir,
            diffFileName = "diffs.txt"
        )

    # freezer.env2File()
    file1 = wdir / "env_ipython.txt"
    file2 = wdir / "env_python.txt"
    # commonKeys= comparer.commonKeys(file1, file2, True)
    comparer.compareEnvs(file1, file2, True)
