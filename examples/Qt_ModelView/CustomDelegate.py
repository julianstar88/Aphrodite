# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:46:05 2020

@author: Julian
"""

from PyQt5 import QtWidgets, QtCore
from CustomComponents import CustomStandardEditorWidget

class CustomItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.data = None
        self.view = None
        self.closeEditor.connect(self.onClosed)
        self.commitData.connect(self.onCommitData)

        self.size = {"width":200, "height":65}

    def createEditor(self, parent, option, index):
        message = self.__createMessage(index)
        editor = CustomStandardEditorWidget(message, parent=parent)
        return editor

    def __createMessage(self, index):
        col = index.column()
        if col == 1:
            message = "Sets [None]:"
        elif col == 2:
            message = "Repetitions [None]:"
        else:
            message = "Weight [kg]:"
        return message

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            row = index.row()
            col = index.column()
            self.view = model.parent()
            self.data = [row,
                         col,
                         self.view.rowHeight(row),
                         self.view.columnWidth(col)]
            self.view.setRowHeight(row, self.size["height"])
            self.view.setColumnWidth(col, self.size["width"])
        return False

    def setEditorData(self, editor, index):
        editor.edit.setText(index.data())

    def setModelData(self, editor, model, index):
        item = model.itemFromIndex(index)
        item.setData(editor.edit.text(), False)

    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)


    # slots
    def onClosed(self, editor, hint):
        self.view.setColumnWidth(self.data[1], self.data[3])
        self.view.setRowHeight(self.data[0], self.data[2])

        self.commitData.emit(editor)

    def onCommitData(self, editor):
        pass