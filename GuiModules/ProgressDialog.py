# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:11:28 2020

@author: Julian
"""
import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtProperty

class ProgressWindow(QtWidgets.QWidget):

    defaultValues = {
            "animateColor": True,
            "labelWordWrap": True,
            "maximum": 0,
            "minimum": 0,
            "ProgressWindowMinSize": QtCore.QSize(50, 50),
            "message": None,
            "value": None
        }

    def __init__(self, parent, *args,
                 animateColor = None,
                 maximum = None,
                 minimum = None,
                 message = None,
                 value = None,
                 wordWrap = None):

        super().__init__(parent, *args)
        self._animateColor = None
        self._parent = None
        self._mainWidget = None
        self._mainLayout = None
        self._maximum = None
        self._message = None
        self._minimum = None
        self._layout = None
        self._label = None
        self._progress = None
        self._value = None
        self._wordWrap = None

        # set a frameless Tool-Window. This Window also gets deleted if closed
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.Window, True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        # create progress window components
        self._mainLayout = QtWidgets.QGridLayout(self)
        self._mainWidget = QtWidgets.QWidget(self)
        self._layout = QtWidgets.QGridLayout(self._mainWidget)
        self._progress = ProgressWheel()
        self._label = QtWidgets.QLabel()

        self.setParent(parent)

        if message:
            self.setMessage(message)
        else:
            self.setMessage(type(self).defaultValues["message"])

        if animateColor:
            self.setAnimateColor(animateColor)
        else:
            self.setAnimateColor(type(self).defaultValues["animateColor"])

        if maximum:
            self.setMaximum(maximum)
        else:
            self.setMaximum(type(self).defaultValues["maximum"])

        if minimum:
            self.setMinimum(minimum)
        else:
            self.setMinimum(type(self).defaultValues["minimum"])

        if value:
            self.setValue(value)
        else:
            self.setValue(type(self).defaultValues["value"])

        if wordWrap:
            self.setWordWrap(wordWrap)
        else:
            self.setWordWrap(type(self).defaultValues["labelWordWrap"])

        self.setupWindow()
        self.setupPosition()
        self.setupStyle()

        self.show()

    def animateColor(self):
        return self._animateColor

    def paintEvent(self, event):
        self.setupPosition()
        return super().paintEvent(event)

    def message(self):
        return self._message

    def maximum(self):
        return self._maximum

    def minimum(self):
        return self._minimum

    def parent(self):
        return self._parent

    def radius(self):
        return self._progress.radius()

    def resetProgressWheel(self):
        self._progress.reset()

    def setAnimateColor(self, enable):
        if self._progress.setAnimateColor(enable):
            value = bool(enable)
            self._animateColor = value
            return True

    def setMaximum(self, maximum):
        if self._progress.setMaximum(maximum):
            self._maximum = maximum
            return True
        else:
            return False

    def setMessage(self, message):
        self._message = message
        self.updateMessage()
        return True

    def setMinimum(self, minimum):
        if self._progress.setMinimum(minimum):
            self._minimum = minimum
            return True
        else:
            return False

    def setParent(self, parent):
        self._parent = parent
        return True

    def setRadius(self, r):
        return self._progress.setRadius(r)

    def setupPosition(self):
        parentPos = self.parent().pos()
        parentSize = self.parent().size()
        parentOrigin = [
                round(parentSize.width()/2 + parentPos.x()),
                round(parentSize.height()/2 + parentPos.y())
            ]
        ownSize = self.size()
        newPosition = [
                round(parentOrigin[0] - ownSize.width()/2),
                round(parentOrigin[1] - ownSize.height()/2)
            ]

        self.move(newPosition[0], newPosition[1])
        return True

    def setupStyle(self):
        self.setStyleSheet(
                """
                QWidget {background-color: rgba(119, 136, 153, 80%)}
                """
            )
        self._label.setStyleSheet(
                """
                QLabel {background-color: rgba(0, 0, 0, 0%)}
                """
            )
        return True

    def setupWindow(self):
        self.setMinimumSize(type(self).defaultValues["ProgressWindowMinSize"])
        self.setMaximumSize(self.parent().size())

        self._mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self._layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self._label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self._label.setWordWrap(self.wordWrap())
        self._label.setText(self.message())

        self._mainLayout.addWidget(self._mainWidget, 1, 1)
        self._layout.addWidget(self._progress, 1, 1)

        self._layout.addWidget(self._label, 1, 2)
        return True

    def setValue(self, value):
        if self._progress.setValue(value):
            self._value = value
            return True
        else:
            return False

    def setWordWrap(self, enabled):
        value = bool(enabled)
        self._wordWrap = value
        return True

    def updateMessage(self):
        self._layout.removeWidget(self._label)
        self._label.deleteLater()

        if self.message():
            self._label = QtWidgets.QLabel()

            self._label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            # setting the wordwrap property of self._label fails by instantiating
            # the ProgressWindow. this is caused by invoking
            # self.setMessage() (which calls updateMessage()) before set.WordWrap().
            # updateMessage calls itself self.setMessage(). At this time self.wordWrap()
            # returns None because yet it has not been set to a default value.
            try:
                self._label.setWordWrap(self.wordWrap())
            except TypeError:
                pass

            self._label.setText(self.message())

            self._layout.addWidget(self._label, 1, 2)
            self.setupStyle()

        return True

    def value(self):
        return self._value

    def wordWrap(self):
        return self._wordWrap

class ProgressWheel(QtWidgets.QLabel):

    defaultValues = {
            "angleDelta": 240,
            "animateColor": True,
            "animationDuration": 1000,
            "maximum": 0,
            "minimum": 0,
            "ProgressWheelMinSize": QtCore.QSize(50, 50),
            "radius": 15,
            "startAngle": 0,
            "value": None,
            "wheelColor": "firebrick",
            "wheelColorHsv": 0,
        }

    def __init__(self, *args,
                 angleDelta = None,
                 animationDuration = None,
                 maximum = None,
                 minimum = None,
                 radius = None,
                 startAngle = None,
                 wheelColor = None,
                 animateColor = True,
                 value = None):

        super().__init__(*args)

        self._animateColor = None
        self._angleDelta = None
        self._animationDuration = None
        self._colorAnimation = None
        self._progressAnimation = None
        self._radius = None
        self._startAngle = None
        self._wheelColor = None
        self._wheelColorHsv = None
        self._value = None
        self._minimum = 0
        self._maximum = 0

        if animateColor:
            self.setAnimateColor(animateColor)
        else:
            self.setAnimateColor(type(self).defaultValues["animateColor"])
        if angleDelta:
            self.setAngleDelta(angleDelta)
        else:
            self.setAngleDelta(type(self).defaultValues["angleDelta"])
        if animationDuration:
            self.setAnimationDuration(animationDuration)
        else:
            self.setAnimationDuration(type(self).defaultValues["animationDuration"])
        if startAngle:
            self.setStartAngle(startAngle)
        else:
            self.setStartAngle(type(self).defaultValues["startAngle"])
        if maximum:
            self.setMaximum(maximum)
        else:
            self.setMaximum(type(self).defaultValues["maximum"])
        if minimum:
            self.setMinimum(minimum)
        else:
            self.setMinimum(type(self).defaultValues["minimum"])

        if radius:
            self.setRadius(radius)
        else:
            self.setRadius(type(self).defaultValues["radius"])
        if value:
            self.setValue(value)
        else:
            self.setValue(type(self).defaultValues["value"])
        if wheelColor:
            self.setWheelColor(wheelColor)
        else:
            self.setWheelColor(type(self).defaultValues["wheelColor"])

        self.setWheelColorHsv(type(self).defaultValues["wheelColorHsv"])

        self.setupStyle()
        self.setupWindow()

        self.__initAnimation()
        self.__runColorAnimation()
        self.__runProgressAnimation()

    def __initAnimation(self):
        subAnimation_1 = QtCore.QPropertyAnimation(self, b"angle")
        subAnimation_1.setDuration(self.animationDuration())
        subAnimation_1.setStartValue(0)
        subAnimation_1.setLoopCount(-1)
        subAnimation_1.setEndValue(360)

        subAnimation_2 = QtCore.QPropertyAnimation(self, b"colorHsv")
        subAnimation_2.setDuration(5000)
        subAnimation_2.setStartValue(0)
        subAnimation_2.setLoopCount(-1)
        subAnimation_2.setEndValue(360)

        self._progressAnimation = subAnimation_1
        self._colorAnimation = subAnimation_2
        return True

    def __runColorAnimation(self):
        if self.animateColor():
            if self._colorAnimation:
                self._colorAnimation.start()
                return True
            else:
                return False

        else:
            if self._colorAnimation:
                self._colorAnimation.stop()
            return False

    def __runProgressAnimation(self):
        if self.maximum() == self.minimum():
            if self._progressAnimation:
                self._progressAnimation.start()
                return True
            else:
                return False
        else:
            if self._progressAnimation:
                self._progressAnimation.stop()
            return False

    def animateColor(self):
        return self._animateColor

    def angleDelta(self):
        return self._angleDelta

    def animationDuration(self):
        return self._animationDuration

    def circle(self, phi, radius):
        return [radius*np.cos(phi), radius*np.sin(phi)]

    def maximum(self):
        return self._maximum

    def minimum(self):
        return self._minimum

    def radius(self):
        return self._radius

    def reset(self):
        self.setAnimateColor(type(self).defaultValues["animateColor"])
        self.setValue(type(self).defaultValues["value"])
        self.setMaximum(type(self).defaultValues["maximum"])
        self.setMinimum(type(self).defaultValues["minimum"])

    def startAngle(self):
        return self._startAngle

    def setAnimateColor(self, enable):
        value = bool(enable)
        self._animateColor = value
        self.__runColorAnimation()
        return True

    def setAngleDelta(self, delta):
        x = delta*np.pi/180
        self._angleDelta = x
        self.update()
        return True

    def setAnimationDuration(self, duration):
        self._animationDuration = duration
        return True

    def setMaximum(self, maximum):
        if (maximum < 0) and (maximum < self.minimum()):
            return False
        self._maximum = maximum
        self.__runProgressAnimation()
        return True

    def setMinimum(self, minimum):
        if (minimum < 0) and (minimum > self.maximum()):
            return False
        self._minimum = minimum
        self.__runProgressAnimation()
        return True

    def setRadius(self, r):

        if isinstance(r, str):
            if r == "auto":
                s = list()
                s.append(self.width())
                s.append(self.height())
                s = min(s)
                value = round(s/3)
                self._radius = value
                return True

        self._radius = int(r)
        return True

    def setStartAngle(self, phi):
        x = phi*np.pi/180
        self._startAngle = x
        self.update()
        return True

    def setupStyle(self):
        self.setStyleSheet(
                """
                ProgressWheel {background-color:rgba(0, 0, 0, 0%)}
                """
            )

    def setupWindow(self):
        self.setMinimumSize(type(self).defaultValues["ProgressWheelMinSize"])

    def setValue(self, value):
        if not value:
            self._value = None
            self.setAngleDelta(type(self).defaultValues["angleDelta"])
            return True
        if (value > self.maximum()) and (value < self.minimum()):
            return False

        self._value = value
        try:
            percent = (self.value()-self.minimum())/(self.maximum()-self.minimum())
        except ZeroDivisionError:
            percent = 0

        angleDelta = round(360*percent)
        self.setAngleDelta(angleDelta)
        return True

    def setWheelColor(self, color):
        self._wheelColor = QtGui.QColor(color)
        return True

    def setWheelColorHsv(self, hue):
        value = int(hue)
        self._wheelColorHsv = value
        self.update()
        return True

    def value(self):
        return self._value

    def wheelColor(self):
        return self._wheelColor

    def wheelColorHsv(self):
        return self._wheelColorHsv

    angle = pyqtProperty(
            float,
            fget = startAngle,
            fset = setStartAngle
        )
    colorHsv = pyqtProperty(
            int,
            fget = wheelColorHsv,
            fset = setWheelColorHsv
        )

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()

        pen.setWidth(3)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        if self.animateColor():
            pen.setColor(
                    QtGui.QColor.fromHsv(
                            self.wheelColorHsv(),
                            255,
                            255
                        )
                )
        else:
            pen.setColor(self.wheelColor())

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        origin = [self.width()/2, self.height()/2]

        for i in np.linspace(self.startAngle(), self.startAngle() + self.angleDelta(), int(1e2)):
            pos = self.circle(i, self.radius())
            point = QtCore.QPointF(pos[0] + origin[0], pos[1] + origin[1])
            painter.drawPoint(point)

class ModuleTest(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUI()
        self.setupStyle()

        message = "progress wheel test..."
        self.progress = ProgressWindow(self)
        self.progress.setRadius("auto")
        self.progress.setWordWrap(False)
        self.progress.setMessage(message)

    def closeEvent(self, event):
        self.progress.deleteLater()
        super().closeEvent(event)

    def setupUI(self):
        self.setWindowTitle("ProgressWindow Test...")
        self.setGeometry(500, 300, 500, 500)

        self.show()

    def setupStyle(self):
        self.setStyleSheet(
                """
                Main {background-color: rgba(255, 255, 255, 100%)}
                """
            )

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ModuleTest()
    sys.exit(qapp.exec_())