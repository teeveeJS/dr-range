import tkinter as tk
from tkinter import simpledialog


class NoteDialog:
    def __init__(self, master, existing_notes):
        self.master = master
        self.top = tk.Toplevel(self.master)
        self.top.title("Notes")

        self.e = tk.Text(self.top, height=12, width=50)
        self.e.insert(tk.END, existing_notes)
        self.e.grid(row=0, column=0, columnspan=2)

        self.b = tk.Button(self.top, text="Ok", command=self.ok)
        self.b.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=20, pady=3)
        self.bc = tk.Button(self.top, text="Cancel", command=self.canc)
        self.bc.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=20, pady=3)
    def ok(self):
        self.master.notes = self.e.get("1.0", tk.END)

        self.canc()
    def canc(self):
        self.master.focus_set()
        self.top.destroy()
