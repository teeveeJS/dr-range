import tkinter as tk

from range_viewer import RangeViewer
from range_table import RangeTable


if __name__ == '__main__':
    root = tk.Tk()
    app = RangeViewer(master=root)
    app.mainloop()
