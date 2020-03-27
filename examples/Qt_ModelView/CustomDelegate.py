# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:46:05 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore
from CustomComponents import standardEditorWidget

class CustomItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent = None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        return standardEditorWidget(parent)

    def setEditorData(self, editor, index):
        editor.edit.setText(index.data())

    def setModelData(self, editor, model, index):
        item = model.itemFromIndex(index)
        item.setData(editor.edit.text(), False)

    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)
        if index.column() > 0:
            editor.setMinimumSize(200, 100)