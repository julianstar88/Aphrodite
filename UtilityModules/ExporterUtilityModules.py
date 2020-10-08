# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:54:40 2020

@author: Julian
"""
from Utility_Function_Library.converter import ColorConverter
from UtilityModules.MiscUtilities import ModelInputValidation

def layoutTemplate(exporter):
        
    """property configuration"""
    wb = exporter.workBook()
    props = exporter.layoutProperties()
    headerRows = 6
    headerStartRow = props["headerStartRow"]
    tableHeaderRows = 1
    endRow = props["layoutMaxRows"]
    tableBodyStartRow = headerRows + tableHeaderRows
    tableBodyRows = endRow - tableBodyStartRow
    maxCols = props["layoutMaxCols"]
    borderColor = "black"
    backgroundColor1 = "gray"
    backgroundColor2 = "white"
    borderStyleThinn = 1
    borderStyleThick = 2
        
    """ create a colorconverter"""
    converter = ColorConverter()
    converter.interpretation = "python"
    converter.colorType = "RGB"

    """customize worksheet"""
    ws = wb.add_worksheet("Trainingsplan")
    ws.set_paper(9) # setup A4 format
    ws.set_margins(
            left = 0.25,
            right = 0.25,
            top = 0.75,
            bottom = 0.75
        )
    ws.center_horizontally()

    """header"""
    
    # header border line with style 2 (thick)
    start = headerStartRow
    for n in range(start, start + headerRows):
        for m in range(maxCols):
            background_format = wb.add_format(
                    {
                        "bg_color": "white"
                     }
                )
            ws.write(n, m, None, background_format)
            if n == start:
                if m == 0:
                    top_format = wb.add_format(
                            {
                                "top": borderStyleThick,
                                "left": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, top_format)
                elif m == maxCols - 1:
                    top_format = wb.add_format(
                            {
                                "top": borderStyleThick,
                                "right": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, top_format)
                else:
                    top_format = wb.add_format(
                            {
                                "top": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, top_format)
            if (n > start) and (n < start + headerRows - 1):
                if m == 0:
                    middle_format = wb.add_format(
                            {
                                "left": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, middle_format)
                elif m == maxCols - 1:
                    middle_format = wb.add_format(
                            {
                                "right": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, middle_format)
            if n == start + headerRows - 1:
                if m == 0:
                    bottom_format = wb.add_format(
                            {
                                "bottom": borderStyleThick,
                                "left": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, bottom_format)
                elif m == maxCols - 1:
                    bottom_format = wb.add_format(
                            {
                                "bottom": borderStyleThick,
                                "right": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, bottom_format)
                else:
                    bottom_format = wb.add_format(
                            {
                                "bottom": borderStyleThick,
                                "border_color": borderColor,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, bottom_format)
    
    # header content
    cellRange = "A{}:B{}".format(start + 2, start + 2)
    name_format = wb.add_format(
            {
                "align": "left",
                "valign": "vcenter",
                "bold": True,
                "bottom": borderStyleThick,
                "left": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, "Name", name_format)
    
    cellRange = "D{}:G{}".format(start + 2, start + 2)
    periode_format = wb.add_format(
            {
                "align": "center",
                "valign": "vcenter",
                "bold": True,
                "bottom": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, "Trainingszeitraum", periode_format)
    
    cellRange = "I{}:J{}".format(start + 2, start + 2)
    mode_format = wb.add_format(
            {
                "align": "right",
                "valign": "vcenter",
                "bold": True,
                "bottom": borderStyleThick,
                "right": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, "Trainingsmodus", mode_format)
    
    time_format = wb.add_format(
            {
                "align": "left",
                "valign": "vcenter",
                "bold": True,
                "bg_color": backgroundColor2
            }
        )
    cellRange = "D{}:E{}".format(start + 3, start + 3)
    ws.merge_range(cellRange, "Anfang:", time_format)
    cellRange = "D{}:E{}".format(start + 4, start + 4)
    ws.merge_range(cellRange, "Ende:", time_format)
    
    """table header"""
    start = start + headerRows
    
    # table header border line style 2 (thick)
    for m in range(maxCols):
        if m == 0:
            border_format = wb.add_format(
                    {
                        "top": borderStyleThick,
                        "bottom": borderStyleThick,
                        "left": borderStyleThick,
                        "border_color": borderColor,
                        "bg_color": backgroundColor1
                    }
                )
            ws.write(start, m, None, border_format)
        elif m == maxCols - 1:
            border_format = wb.add_format(
                    {
                        "top": borderStyleThick,
                        "bottom": borderStyleThick,
                        "right": borderStyleThick,
                        "border_color": borderColor,
                        "bg_color": backgroundColor1
                    }
                )
            ws.write(start, m, None, border_format)
        else:
            border_format = wb.add_format(
                    {
                        "top": borderStyleThick,
                        "bottom": borderStyleThick,
                        "border_color": borderColor,
                        "bg_color": backgroundColor1
                    }
                )
            ws.write(start, m, None, border_format)
            
    # table header content
    cellRange = "A{}:B{}".format(start + 1, start + 1)
    cell_format = wb.add_format(
            {
                "align": "center",
                "valign": "vcenter",
                "top": borderStyleThick,
                "bottom": borderStyleThick,
                "left": borderStyleThick,
                "bold": True,
                "bg_color": backgroundColor1
            }
        )
    ws.merge_range(cellRange, "Übung", cell_format)
    
    cellRange = "C{}".format(start + 1)
    cell_format = wb.add_format(
            {
                "align": "center",
                "valign": "vcenter",
                "top": borderStyleThick,
                "bottom": borderStyleThick,
                "bold": True,
                "bg_color": backgroundColor1
            }
        )
    ws.write(cellRange, "Sätze", cell_format)
    
    cellRange = "D{}".format(start + 1)
    cell_format = wb.add_format(
            {
                "align": "center",
                "valign": "vcenter",
                "top": borderStyleThick,
                "bottom": borderStyleThick,
                "bold": True,
                "bg_color": backgroundColor1
            }
        )
    ws.write(cellRange, "Whlg.", cell_format)
    
    for m in range(4, maxCols):
        week = m - 3
        if m == maxCols - 1:
            cell_format = wb.add_format(
                    {
                        "align": "center",
                        "valign": "vcenter",
                        "top": borderStyleThick,
                        "bottom": borderStyleThick,
                        "right": borderStyleThick,
                        "bold": True,
                        "bg_color": backgroundColor1
                    }
                )
            ws.write(
                    start, m, 
                    "W{}".format(week), 
                    cell_format
                )
        else:
            cell_format = wb.add_format(
                    {
                        "align": "center",
                        "valign": "vcenter",
                        "top": borderStyleThick,
                        "bottom": borderStyleThick,
                        "bold": True,
                        "bg_color": backgroundColor1
                    }
                )
            ws.write(
                    start, m, 
                    "W{}".format(week), 
                    cell_format
                )

    """table body"""
    start = start + tableHeaderRows
    
    # table body border style 2 (thick)
    for n in range(start, start + tableBodyRows):
        for m in range(maxCols):
            if n == start:
                if m <= 1:
                    top_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThick,
                                "left": borderStyleThick,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    cellRange = "A{}:B{}".format(n + 1, n + 1)
                    ws.merge_range(cellRange, None, top_format)
                elif (m > 1) and (m <= 3):
                    top_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThick,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    ws.write(n, m, None, top_format)
                elif m == maxCols - 1:
                    top_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThick,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThick,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, top_format)
                else:
                    top_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThick,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, top_format)
            if (n > start) and (n < start + tableBodyRows - 1):
                if m <= 1:
                    middle_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThick,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    cellRange = "A{}:B{}".format(n + 1, n + 1)
                    ws.merge_range(cellRange, None, middle_format)
                elif (m > 1) and (m <= 3):
                    middle_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    ws.write(n, m, None, middle_format)
                elif m == maxCols - 1:
                    middle_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThick,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, middle_format)
                else:
                    middle_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThinn,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, middle_format)
            if n == start + tableBodyRows - 1:
                if m <= 1:
                    bottom_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThick,
                                "bottom": borderStyleThick,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    cellRange = "A{}:B{}".format(n + 1, n + 1)
                    ws.merge_range(cellRange, None, bottom_format)
                elif (m > 1) and (m <= 3):
                    bottom_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThick,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor1
                            }
                        )
                    ws.write(n, m, None, bottom_format)
                elif m == maxCols - 1:
                    bottom_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThick,
                                "right": borderStyleThick,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, bottom_format)
                else:
                    bottom_format = wb.add_format(
                            {
                                "align": "center",
                                "valign": "vcenter",
                                "top": borderStyleThinn,
                                "left": borderStyleThinn,
                                "bottom": borderStyleThick,
                                "right": borderStyleThinn,
                                "bg_color": backgroundColor2
                            }
                        )
                    ws.write(n, m, None, bottom_format)
                    
    layoutInformation = {
            "headerStartRow": headerStartRow,
            "routineStartRow": tableBodyStartRow,
            "layoutMaxRows": endRow,
            "layoutMaxCols": maxCols
        }
    
    return ws, layoutInformation

def populateTemplate(exporter):
    
    """property configuration"""
    wb = exporter.workBook()
    ws = exporter.workSheet()
    routineData, alternativeData, noteData = exporter.dataFromDatabase()
    validator = ModelInputValidation()
    
    props = exporter.layoutProperties()
    headerStartRow = props["headerStartRow"]
    routineStartRow = props["routineStartRow"]
    alternativeStartRow = props["alternativeStartRow"]
    layoutMaxRows = props["layoutMaxRows"]
    layoutMaxCols = props["layoutMaxCols"]
    borderColor = "black"
    backgroundColor1 = "gray"
    backgroundColor2 = "white"
    borderStyleThinn = 1
    borderStyleThick = 2

    
    """set header data"""
    cellRange = "A{}:B{}".format(
            headerStartRow + 3,
            headerStartRow + 3
        )
    cellFormat = wb.add_format(
            {
                "align": "left",
                "valign": "vcenter",
                "top": borderStyleThick,
                "left": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, exporter.name(), cellFormat)
    
    cellRange = "F{}:G{}".format(
            headerStartRow + 3,
            headerStartRow + 3
        )
    cellFormat = wb.add_format(
            {
                "align": "right",
                "valign": "vcenter",
                "top": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, exporter.trainingPeriode()[0], cellFormat)
    
    cellRange = "F{}:G{}".format(
            headerStartRow + 4,
            headerStartRow + 4
        )
    cellFormat = wb.add_format(
            {
                "align": "right",
                "valign": "vcenter",
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, exporter.trainingPeriode()[1], cellFormat)
    
    cellRange = "H{}:J{}".format(
            headerStartRow + 3,
            headerStartRow + 3
        )
    cellFormat = wb.add_format(
            {
                "align": "right",
                "valign": "vcenter",
                "right": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2
            }
        )
    ws.merge_range(cellRange, exporter.trainingMode(), cellFormat)
    
    """set routine data"""
    inputValues = [routineData[i][0] for i in range(len(routineData))]
    
    # exercise names
    for i, val in enumerate(inputValues):
        rowID = i + 1
        
        l = list()
        for alternative in alternativeData:
            if rowID == alternative[0]:
                l.append(alternative[1])
        alternatives = "%s" * len(l)
        alternatives = alternatives % tuple(l)
        
        l = list()
        for note in noteData:
            if rowID == note[0]:
                l.append(note[1])
        notes = "%s" * len(l)
        notes = notes % tuple(l)
        
        f = {
                "align": "left",
                "valign": "vcenter",
                "bg_color": backgroundColor1,
                "border_color": borderColor
            }
        if i == 0:
            f["top"] = borderStyleThick
            f["left"] = borderStyleThick
            f["bottom"] = borderStyleThinn
            f["right"] = borderStyleThinn
        if (i > 0) and (i < len(routineData) - 1):
            f["top"] = borderStyleThinn
            f["left"] = borderStyleThick
            f["bottom"] = borderStyleThinn
            f["right"] = borderStyleThinn
        if i == len(routineData) - 1:
            f["top"] = borderStyleThinn
            f["left"] = borderStyleThick
            f["bottom"] = borderStyleThinn
            f["right"] = borderStyleThinn
        
        superFormat = wb.add_format({"font_script": 1})
        subFormat = wb.add_format({"font_script": 2})
        cellFormat = wb.add_format(f)
        value = [val]
        if alternatives:
            value.append(superFormat)
            value.append(alternatives)
        if notes:
            value.append(subFormat)
            value.append(notes)
        
        ws.merge_range(
                routineStartRow + i, 
                0, 
                routineStartRow + i, 
                1, 
                None, 
                cellFormat
            )
        
        if len(value) == 1:
            ws.write(
                    routineStartRow + i,
                    0,
                    *value,
                    cellFormat
                )
        else:
            ws.write_rich_string(
                    routineStartRow + i, 
                    0, 
                    *value,
                    cellFormat
                )
    
    # excercise values
    for n, row in enumerate(routineData):
        row = row[1:-1]
        del row[2]
        
        for m, val in enumerate(row):
            # if values are readalbe as numeric values in  a
            # 'ModelInputValidation' manner, convert them into integer
            # (prevent excel from throwing a warning for writing numers as 
            # string)
            if validator.checkValue(val):
                val = validator.readValue2(val)[0]
            
            f = {
                    "align": "left",
                    "valign": "vcenter",
                    "border_color": borderColor
                }
            if n == 0:
                if m <= 1:
                    f["border"] = borderStyleThinn
                    f["top"] = borderStyleThick
                    f["bg_color"] = backgroundColor1
                if (m > 1) and (m < len(row) - 1):
                    f["border"] = borderStyleThinn
                    f["top"] = borderStyleThick
                    f["bg_color"] = backgroundColor2
                if m == len(row) - 1:
                    f["border"] = borderStyleThinn
                    f["top"] = borderStyleThick
                    f["right"] = borderStyleThick
                    f["bg_color"] = backgroundColor2
            else:
                if m <= 1:
                    f["border"] = borderStyleThinn
                    f["bg_color"] = backgroundColor1
                if (m > 1) and (m < len(row) - 1):
                    f["border"] = borderStyleThinn
                    f["bg_color"] = backgroundColor2
                if m == len(row) - 1:
                    f["border"] = borderStyleThinn
                    f["right"] = borderStyleThick
                    f["bg_color"] = backgroundColor2
            cellFormat = wb.add_format(f)
            ws.write(
                    routineStartRow + n,
                    2 + m,
                    val,
                    cellFormat
                )
            
    """set alternative data"""
    alternativeStartRow = routineStartRow + len(routineData) + 3
    
    cellFormat = wb.add_format(
            {
                "align": "left",
                "valign": "vcenter",
                "top": borderStyleThinn,
                "left": borderStyleThick,
                "bottom": borderStyleThinn,
                "right": borderStyleThinn,
                "border_color": borderColor,
                "bg_color": backgroundColor1,
                "bold": True
            }
        )
    ws.write(
            alternativeStartRow,
            0,
            "Alternativen:",
            cellFormat
        )
    
    alternativeStartRow += 1
    
    # alternative exercise names
    for i, val in enumerate(alternativeData):
        value = val[1] + ") " + val[3]
        cellFormat = wb.add_format(
                {
                    "align": "left",
                    "valign": "vcenter",
                    "border": borderStyleThinn,
                    "left": borderStyleThick,
                    "border_color": borderColor,
                    "bg_color": backgroundColor1
                }
            )
        ws.write(
                alternativeStartRow + i,
                0,
                value,
                cellFormat
            )
    
    # alternative exercise values
    for n, row in enumerate(alternativeData):
        row = row[4:-1]
        del row[2]
        
        for m, val in enumerate(row):
            # if values are readable as numeric values in a 
            # 'ModelInputValidation' manner, convert them into integer
            # (prevent excel from throwing a warning for writing numbers
            # as string)
            if validator.checkValue(val):
                val = validator.readValue2(val)[0]
            
            f = {
                    "align": "left",
                    "valign": "vcenter",
                    "border_color": borderColor
                }
            if m <= 1:
                f["border"] = borderStyleThinn
                f["bg_color"] = backgroundColor1
            if (m > 1) and (m < len(row) - 1):
                f["border"] = borderStyleThinn
                f["bg_color"] = backgroundColor2
            if m == len(row) - 1:
                f["border"] = borderStyleThinn
                f["right"] = borderStyleThick
                f["bg_color"] = backgroundColor2
            cellFormat = wb.add_format(f)
            ws.write(
                    alternativeStartRow + n,
                    2 + m,
                    val,
                    cellFormat
                )
            
    """set note data"""
    cellFormat = wb.add_format(
            {
                "align": "left",
                "valign": "vcenter",
                "top": borderStyleThick,
                "border_color": borderColor,
                "bg_color": backgroundColor2,
                "bold": True
            }
        )
    ws.write(
            layoutMaxRows,
            0,
            "Notizen:",
            cellFormat
        )
    ws.merge_range(
        layoutMaxRows,
        1,
        layoutMaxRows,
        layoutMaxCols - 1,
        None,
        cellFormat
        )
    layoutMaxRows += 1
    
    # note labels
    inputValues = [noteData[i][1] for i in range(len(noteData))]
    for i, val in enumerate(inputValues):
        value = val + ")"
        cellFormat = wb.add_format(
                {
                    "align": "left",
                    "valign": "vcenter",
                    "bg_color": backgroundColor2
                }
            )
        ws.write(
                layoutMaxRows + i,
                0,
                value,
                cellFormat 
            )
    
    # note values
    inputValues = [noteData[i][3] for i in range(len(noteData))]
    for i, val in enumerate(inputValues):
        cellFormat = wb.add_format(
                {
                    "align": "left",
                    "valign": "vcenter",
                    "bg_color": backgroundColor2
                }
            )
        ws.merge_range(
                layoutMaxRows + i,
                1,
                layoutMaxRows + i,
                layoutMaxCols - 1,
                val,
                cellFormat
            )