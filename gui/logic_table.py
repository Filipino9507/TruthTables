import tkinter as tk
from tkinter.font import BOLD, ITALIC
from typing import List, Union


class LogicTable(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.entries: List[List[tk.Widget]] = []

    def _clear(self):
        if len(self.entries) == 0:
            return
        rcount, ccount = len(self.entries), len(self.entries[0])
        for i in range(rcount):
            for j in range(ccount):
                self.entries[i][j].grid_forget()
        self.entries: List[List[tk.Widget]] = []

    def populate(self, data: List[List[Union[str, bool]]]):
        self._clear()
        rcount, ccount = len(data), len(data[0])
        self.entries = [[None for _ in range(ccount)] for _ in range(rcount)]
        strvars = [[None for _ in range(ccount)] for _ in range(rcount)]
        for i in range(rcount):
            for j in range(ccount):
                strvars[i][j] = tk.StringVar(value=data[i][j])
                font_weight = "bold" if i == 0 else "normal"
                self.entries[i][j] = tk.Entry(
                    self, width=10, textvariable=strvars[i][j], font=("Helvetica", 16, font_weight))
                self.entries[i][j].grid(row=i, column=j)
                self.entries[i][j].configure(state="readonly")
