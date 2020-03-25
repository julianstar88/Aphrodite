# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:38:45 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore
# from HelperModules import createCanvas, createQPixmap

class CustomHeader(QtWidgets.QHeaderView):
    """
    implementation from: https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget

    """

    ObjectType = "CustomHeader"

    def __init__(self, parent):
        super().__init__(QtCore.Qt.Horizontal, parent)
        self.qpixmaps = list()

    def paintSection(self, painter, rect, index):

        if not rect.isValid():
            return

        opt = QtWidgets.QStyleOptionHeader()
        self.initStyleOption(opt)

        opt.rect = rect
        opt.section = index
        opt.text = ""

        # highlight if mouse is over section
        # mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        # if rect.contains(mouse_pos):
        #     opt.state |= QtGui.QStyle.State_MouseOver

        painter.save()
        self.style().drawControl(QtWidgets.QStyle.CE_Header, opt, painter, self)
        painter.restore()

        qpixmap = self.qpixmaps[index]

        # for horizontal Centering
        # xpix = (rect.width() - qpixmap.size().width()) / 2 + rect.x()

        # for left alignment
        xpix = rect.x()

        # for vertical centering
        ypix = (rect.height() - qpixmap.size().height()) / 2

        rect = QtCore.QRect(xpix, ypix, qpixmap.size().width(),
                            qpixmap.size().height())
        painter.drawPixmap(rect, qpixmap)

    def sizeHint(self):

        baseSize = QtWidgets.QHeaderView.sizeHint(self)

        baseHeight = baseSize.height()
        if len(self.qpixmaps):
            for pixmap in self.qpixmaps:
               baseHeight = max(pixmap.height(), baseHeight)
        baseSize.setHeight(baseHeight)

        self.parentWidget().repaint()

        return baseSize