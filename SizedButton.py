import tkinter as tk
from tkinter import ttk


class SizedButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None, text="", command=None, style=None):
        ttk.Frame.__init__(self, parent, height=height, width=width, style="SizedButton.TFrame")

        self.pack_propagate(False)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1, padx=10, pady=5)

    def set_text(self, text):
        self._btn.config(text=text)

    def get_text(self):
        return self._btn.cget('text')

    def set_cmd(self, cmd):
        self._btn.config(command=cmd)
