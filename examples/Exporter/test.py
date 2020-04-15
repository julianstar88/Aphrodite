# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:54:40 2020

@author: Julian
"""
import openpyxl
from openpyxl.styles import Alignment, Border, Color, Font, PatternFill, Side
from Utility_Function_Library.converter import ColorConverter

def setAlignment(ws, cellRange,
                 horizontal = "center",
                 vertical = "center"):

    cellRange = ws[cellRange]
    for row in cellRange:
        for cell in row:
            cell.alignment = Alignment(
                    horizontal = horizontal,
                    vertical = vertical
                )

def setBackground(ws, cellRange,
                  fill_type = None,
                  fgColor = Color(),
                  bgColor = Color(),
                  start_color = None,
                  end_color = None):

    cellRange = ws[cellRange]
    for i, row in enumerate(cellRange):
        for n, cell in enumerate(row):
            cell.fill = PatternFill(
                    fill_type = fill_type,
                    fgColor = fgColor,
                    bgColor = bgColor,
                    start_color = start_color,
                    end_color = end_color
                )

def setBorder(ws, cellRange,
              borderStyle = "thick",
              gridStyle = None):

    cellRange = ws[cellRange]

    if len(cellRange) == 1:
        row = cellRange[0]
        for i, cell in enumerate(row):
            if i == 0:
                cell.border = Border(
                        top = Side(
                                border_style = borderStyle
                            ),
                        left = Side(
                                border_style = borderStyle
                            ),
                        bottom = Side(
                                border_style = borderStyle
                            )
                    )
                if gridStyle:
                    cell.border = Border(
                            top = Side(
                                    border_style = borderStyle
                                ),
                            left = Side(
                                    border_style = borderStyle
                                ),
                            bottom = Side(
                                    border_style = borderStyle
                                ),
                            right = Side(
                                    border_style = gridStyle
                                )
                        )
            elif i == len(row)-1:
                cell.border = Border(
                        top = Side(
                                border_style = borderStyle
                            ),
                        bottom = Side(
                                border_style = borderStyle
                            ),
                        right = Side(
                                border_style = borderStyle
                            )
                    )
            else:
                cell.border = Border(
                        top = Side(
                                border_style = borderStyle
                            ),
                        bottom = Side(
                                border_style = borderStyle
                            )
                    )
                if gridStyle:
                    cell.border = Border(
                            top = Side(
                                    border_style = borderStyle
                                ),
                            bottom = Side(
                                    border_style = borderStyle
                                ),
                            right = Side(
                                    border_style = gridStyle
                                )
                        )
        return

    for i, row in enumerate(cellRange):
        for n, cell in enumerate(row):
            if i == 0:
                if n == 0:
                    cell.border = Border(
                            top = Side(
                                    border_style = borderStyle
                                ),
                            left = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                top = Side(
                                        border_style = borderStyle
                                    ),
                                left = Side(
                                        border_style = borderStyle
                                    ),
                                bottom = Side(
                                        border_style = gridStyle
                                    ),
                                right = Side(
                                        border_style = gridStyle
                                    )
                            )
                elif n == len(row)-1:
                    cell.border = Border(
                            top = Side(
                                    border_style = borderStyle
                                ),
                            right = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                top = Side(
                                        border_style = borderStyle
                                    ),
                                right = Side(
                                        border_style = borderStyle
                                    ),
                                bottom = Side(
                                        border_style = gridStyle
                                    )
                            )
                else:
                    cell.border = Border(
                            top = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                top = Side(
                                        border_style = borderStyle
                                    ),
                                bottom = Side(
                                        border_style = gridStyle
                                    ),
                                right = Side(
                                        border_style = gridStyle
                                    )
                            )
            elif i == len(cellRange)-1:
                if n == 0:
                    cell.border = Border(
                        bottom = Side(
                                border_style = borderStyle
                            ),
                        left = Side(
                                border_style = borderStyle
                            )
                        )
                    if gridStyle:
                        cell.border = Border(
                            bottom = Side(
                                    border_style = borderStyle
                                ),
                            left = Side(
                                    border_style = borderStyle
                                ),
                            right = Side(
                                    border_style = gridStyle
                                )
                            )
                elif n == len(row)-1:
                    cell.border = Border(
                            bottom = Side(
                                    border_style = borderStyle
                                ),
                            right = Side(
                                    border_style = borderStyle
                                )
                        )
                else:
                    cell.border = Border(
                            bottom = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                bottom = Side(
                                        border_style = borderStyle
                                    ),
                                right = Side(
                                        border_style = gridStyle
                                    )
                            )
            else:
                if n == 0:
                    cell.border = Border(
                            left = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                left = Side(
                                        border_style = borderStyle
                                    ),
                                bottom = Side(
                                        border_style = gridStyle
                                    ),
                                right = Side(
                                        border_style = gridStyle
                                    )
                            )
                elif n == len(row)-1:
                    cell.border = Border(
                            right = Side(
                                    border_style = borderStyle
                                )
                        )
                    if gridStyle:
                        cell.border = Border(
                                right = Side(
                                        border_style = borderStyle
                                    ),
                                bottom = Side(
                                        border_style = gridStyle
                                    )
                            )
                else:
                    if gridStyle:
                        cell.border = Border(
                                bottom = Side(
                                        border_style = gridStyle
                                    ),
                                right = Side(
                                        border_style = gridStyle
                                    )
                            )

def setGrid(ws, cellRange,
                  gridStyle = "thin"):

    cellRange = ws[cellRange]
    for i, row in enumerate(cellRange):
        for n, cell in enumerate(row):
            if i == len(cellRange)-1:
                if not n == len(row)-1:
                    cell.border = Border(
                            right = Side(
                                    border_style = gridStyle
                                )
                        )
            else:
                if  n == len(row)-1:
                    cell.border = Border(
                            bottom = Side(
                                    border_style = gridStyle
                                )
                        )
                else:
                    cell.border = Border(
                            bottom = Side(
                                    border_style = gridStyle
                                ),
                            right = Side(
                                    border_style = gridStyle
                                )
                        )



if __name__ == "__main__":
    # create Workbook
    converter = ColorConverter()
    converter.interpretation = "openpyxl"
    converter.colorType = "HEX"
    wb = openpyxl.Workbook()

    # customize worksheet
    ws = wb.active
    ws.title = "Trainingsplan"
    ws.column_dimensions["A"].width = 25
    ws.page_margins = openpyxl.worksheet.page.PageMargins(
            left = 0.25,
            right = 0.25,
            top = 0.75,
            bottom = 0.75,
            header = 0.5,
            footer = 0.5
        )
    ws.print_options = openpyxl.worksheet.page.PrintOptions(
            horizontalCentered = True,
            verticalCentered = False
        )

    # header
    ws.cell(2, 1, value = "Name:").font = Font(
            b = True
        )
    ws.cell(3, 1, value = "Julian")
    ws.cell(2, 5, value = "Datum:").font = Font(
            b = True
        )
    ws.cell(3, 5, value = "15.04.2020")
    ws.cell(2, 8, value = "Trainingsmodus:").font = Font(
            b = True
        )
    ws.cell(3, 8, value = "Maximalkraft")
    ws.merge_cells("H2:I2")
    ws.merge_cells("H3:I3")
    setAlignment(ws, "A1:I5")
    setBorder(ws, "A1:I5")
    setBackground(ws, "A1:I5",
                  fill_type = "solid",
                  fgColor = converter.color("white")
            )

    # table header
    ws.cell(6, 1, value = "Übung").font = Font(
            b = True
        )
    ws.cell(6, 2, value = "Sätze").font = Font(
            b = True
        )
    ws.cell(6, 3, value = "Whlg.").font = Font(
            b = True
        )
    ws.cell(6, 4, value = "W1").font = Font(
            b = True
        )
    ws.cell(6, 5, value = "W2").font = Font(
            b = True
        )
    ws.cell(6, 6, value = "W3").font = Font(
            b = True
        )
    ws.cell(6, 7, value = "W4").font = Font(
            b = True
        )
    ws.cell(6, 8, value = "W5").font = Font(
            b = True
        )
    ws.cell(6, 9, value = "W6").font = Font(
            b = True
        )
    setAlignment(ws, "A6:I6")
    setBorder(ws, "A6:I6")
    setBackground(ws, "A6:I6",
                  fill_type = "solid",
                  fgColor = converter.color("gray")
            )

    # table body
    setAlignment(ws, "A7:A40",
            horizontal = "left",
            vertical = "center"
        )
    setAlignment(ws, "B7:I40",
            horizontal = "center",
            vertical = "center"
        )
    borderRange = "A7:I40"
    backgroundRange = "A7:C40"
    setBorder(ws, borderRange,
              borderStyle = "thick",
              gridStyle = "thin"
        )
    setBackground(ws, backgroundRange,
                  fill_type = "solid",
                  fgColor = converter.color("gray")
        )

    # save workbook in designated file
    wb.save("test_trainingroutine.xlsx")


