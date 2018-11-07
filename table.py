#!usr/bin/python
import tkinter as tk
from tkinter import *
from tkinter import ttk

class Table(ttk.Frame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.grid = []
        self.rows = 0
        self.cols = 0

        # Scrollable
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(
            self, orient = 'vertical', command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        self.pack(fill = 'both', expand = True)
        self.canvas.pack(side = LEFT, fill = 'y')
        self.scrollbar.pack(side = LEFT, fill = 'both', expand = True)
        self.canvas.create_window((0,0), window = self.frame, anchor = 'nw')

        self.frame.bind('<Configure>', self.onFrameConfigure)
        self.canvas.bind_all('<MouseWheel>', self.onMouseWheel)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox('all'))
        self.canvas.configure(width = self.frame.winfo_width())

    def onMouseWheel(self, event):
        speed_decrease = 120
        self.canvas.yview_scroll(int(-1*(event.delta/speed_decrease)), 'units')

    def add_field(self, col, row):
        field = ttk.Label(self.frame, text = '', borderwidth = 2)
        field.grid(column = col, row = row)
        return field

    def create_grid(self, cols, rows):
        self.rows = rows
        self.cols = cols
        for i in range(rows):
            fields = [] 
            for j in range(cols):
                fields.append(self.add_field(row = i, col = j))
            self.grid.append(fields)

    def resize_grid(self, cols, rows):
        cols_to_add = cols - self.cols
        rows_to_add = rows - self.rows

        # Add columns
        if cols_to_add > 0:
            for i, row in enumerate(self.grid):
                for j in range(cols_to_add):
                    row.append(self.add_field(row = i, col = self.cols + j))
            self.cols += cols_to_add

        # Add rows
        if rows_to_add > 0:
            for i in range(rows_to_add):
                new_row = []
                for j in range(self.cols):
                    new_row.append(self.add_field(row = self.rows + i, col = j))
                self.grid.append(new_row)
            self.rows += rows_to_add

    def reset_fields(self):
        for rows in self.grid:
            for col in rows:
                col.configure(text = '*')

    def show(self, header, rows):
        col_num = len(header)
        row_num = len(rows) + 1

        # Create new grid, if there is none
        if self.cols == 0 or self.rows == 0:
            self.create_grid(col_num, row_num)
        # Resize grid if it's too small
        elif self.cols < col_num or self.rows < row_num:
            self.resize_grid(col_num, row_num)

        # Reset previous data
        self.reset_fields()

        # Add header data
        for j, col in enumerate(header):
            self.grid[0][j].configure(text = col)

        # Add records data
        for i, row in enumerate(rows):
            cols = str(row).split(';')
            for j, col in enumerate(cols):
                self.grid[i+1][j].configure(text = col)




