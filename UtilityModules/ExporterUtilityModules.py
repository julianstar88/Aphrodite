# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:54:40 2020

@author: Julian
"""
import xlsxwriter
from Utility_Function_Library.converter import ColorConverter

def templateLayout(workbook, endRow):

    if endRow < 6:
        raise ValueError(
                "input of {num} is too small. The 'endRow' argument must be greater or equal than 6".format(
                    num = endRow
                )
            )
    if type(endRow) != int:
        raise TypeError(
                "input of type {input_type_name} does not match the required type {type_name}".format(
                    input_type_name = type(endRow),
                    type_name = type(123)
                )
            )
    if not isinstance(workbook, xlsxwriter.Workbook):
        raise TypeError(
                "input to type <{input_type_name}> does not match {type_name}".format(
                        input_type_name = type(workbook),
                        type_name = xlsxwriter.Workbook
                    )
            )
        
    """ create a colorconverter"""
    converter = ColorConverter()
    converter.interpretation = "python"
    converter.colorType = "RGB"

    """customize worksheet"""
    wb = workbook
    ws = wb.add_worksheet("Trainingsplan")
    ws.set_paper(9) # setup A4 format
    ws.set_margins(
            left = 0.25,
            right = 0.25,
            top = 0.75,
            bottom = 0.75
        )
    ws.center_horizontally()
    
    headerRows = 6
    tableHeaderRows = 1
    tableBodyRows = endRow - (headerRows + tableHeaderRows) 
    maxCols = 10
    borderColor = "black"
    backgroundColor1 = "gray"
    backgroundColor2 = "white"
    borderStyleThinn = 1
    borderStyleThick = 2

    """header"""
    
    # header border line with style 2 (thick)
    start = 0
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
    
if __name__ == "__main__":

    wb = xlsxwriter.Workbook(r"ExporterUtil_test.xlsx")
    
    templateLayout(wb, 40)
    
    wb.close()



