# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:46:05 2020

@author: Julian
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from GuiModules.CustomGuiComponents import CustomStandardEditorWidget

class CustomItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.data = None
        self.view = None
        self.closeEditor.connect(self.onClosed)

        self.size = {"width":100, "height":65}

    def __createMessage(self, index):
        col = index.column()
        row = index.row()
        modeCol = self.parent().model().columnCount()-1
        modeItem = self.parent().model().item(row, modeCol)
        mode = modeItem.data(role = QtCore.Qt.DisplayRole)
        if mode == "gym":
            if col == 1:
                message = "Sets:"
            elif col == 2:
                message = "Repetitions:"
            else:
                message = "$m~([m] = kg)$:"
        elif mode == "interval":
            if col == 1:
                message = "Sets:"
            elif col == 2:
                message = "Repetitions:"
            else:
                message = "$\\overline{v}~([\\overline{v}] = \\frac{km}{h})$"
        elif mode == "distance":
            if col == 1:
                message = "Sets:"
            elif col == 2:
                message = "Repititions:"
            else:
                message = "$s~([s] = km):$"
        else:
            message = "insert value:"
        return message

    def createEditor(self, parent, option, index):
        message = self.__createMessage(index)
        editor = CustomStandardEditorWidget(message, parent = parent)
        return editor

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            row = index.row()
            col = index.column()
            self.view = model.parent()
            self.data = [row,
                         col,
                         self.view.rowHeight(row),
                         self.view.columnWidth(col)]
            self.view.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Fixed)
            self.view.setRowHeight(row, self.size["height"])
            self.view.setColumnWidth(col, self.size["width"])
        return False

    def eventFilter(self, editor, event):
        if event.type() == QtCore.QEvent.Leave:
            self.closeEditor.emit(editor)
        if event.type() == QtCore.QEvent.FocusIn:
            editor.edit.setFocus(QtCore.Qt.MouseFocusReason)
        if isinstance(event, QtGui.QKeyEvent):
            if event.key() == QtCore.Qt.Key_Tab:
                self.closeEditor.emit(editor)
        return super().eventFilter(editor, event)

    def setEditorData(self, editor, index):
        editor.edit.setText(index.data())
        editor.edit.setSelection(0, len(index.data()))

    def setModelData(self, editor, model, index):
        item = model.itemFromIndex(index)
        item.setData(editor.edit.text(), QtCore.Qt.DisplayRole, defaultPurpose = True)

    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)


    # slots
    def onClosed(self, editor, hint):
        self.view.setColumnWidth(self.data[1], self.data[3])
        self.view.setRowHeight(self.data[0], self.data[2])
        for i in range(self.view.horizontalHeader().count()):
            if i != 0:
            #     self.view.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Fixed)
            # else:
                self.view.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                
class BackgroundAlertDelegate(QtWidgets.QStyledItemDelegate):
    
    def __init__(self, model, *args, exerciseLimit = 30):
        super().__init__(*args)
        self._model = model
        self._exerciseLimit = exerciseLimit
        self._backgroundColor = QtGui.QColor(178, 34, 34, 255)
        
    def sumOfSets(self):
        rows = self._model.rowCount()
        sumOfSets = 0
        
        if rows > 0:
            for i in range(rows):
                sets = self._model.item(i, 1).userData()
                try:
                    sets = round(float(sets))
                except:
                    sets = 0
                sumOfSets += sets
            
        return sumOfSets
        
    def paint(self, painter, option, index):

        if not option.rect.isValid():
            return        

        if index.column() == 1:
            sets = self.sumOfSets()
            
            if sets <= self._exerciseLimit:
                brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
            else:
                brush = QtGui.QBrush(self._backgroundColor)
                
            painter.save()
            painter.fillRect(option.rect, brush)
            painter.restore()
            
        super().paint(painter, option, index)
