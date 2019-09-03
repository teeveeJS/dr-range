import tkinter as tk
from tkinter import messagebox
import json
# from range_db import *
import range_db
import range_viewer


class RangeTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Browse Ranges")

        self.master.geometry("500x200")

        self.box_size = 5

        self.initUI()


    def initUI(self):
        self.create_menubar()

        self.init_canvas()

        self.l0 = tk.Label(self.master, text="ID | Name | Hero | Villain | Type | Actions | Table | Notes")
        self.l0.pack()
        self.list_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.master, yscrollcommand=self.list_scroll.set)
        self.listbox.bind("<<ListboxSelect>>", self.preview_range)
        self.list_scroll.config(command=self.listbox.yview)
        self.list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.populate_listbox()



        return


    def create_menubar(self):
        self.menubar = tk.Menu(self.master)

        self.menu_opts = tk.Menu(self.menubar, tearoff=0)
        self.menu_opts.add_command(label="Refresh", command=self.refresh)
        self.menu_opts.add_command(label="Load Range", command=self.return_range)
        self.menu_opts.add_command(label="Load in New Window", command=self.load_new)
        self.menu_opts.add_command(label="Delete Range", command=self.delete_range)
        self.menubar.add_cascade(label="File", menu=self.menu_opts)

        self.positions = [
            ("Any", "any"),
            ("SB", "sb"),
            ("BB", "bb"),
            ("UTG", "utg"),
            ("UTG+1", "utg1"),
            ("MP1", "utg2"),
            ("MP2", "utg3"),
            ("HJ", "utg4"),
            ("CO", "utg5"),
            ("BU", "bu")
        ]

        self.villains = [
            ("Any", "any"),
            ("Optimal", "optimal"),
            ("Loose-Aggressive", "lag"),
            ("Tight-Aggressive", "tag"),
            ("Fish", "fish"),
            ("Nit", "nit"),
            ("Maniac", "manic")
        ]

        self.tables = [
            ("Any", "any"),
            ("Full Ring", "full"),
            ("6 Max", "max6"),
            ("3-Handed", "max3"),
            ("Heads-Up", "hu")
        ]

        self.previous_acts = [
            ("Any", "any"),
            ("Folds to Hero", "open"),
            ("Facing a Raise", "raise"),
            ("One Limper", "limp1"),
            ("Multiple Limpers", "many_limps")
        ]

        self.hero_pos = tk.Menu(self.menubar, tearoff=0)
        self.hero_pos_var = tk.StringVar(self.master)
        self.hero_pos_var.set("any")

        self.villain_pos = tk.Menu(self.menubar, tearoff=0)
        self.villain_pos_var = tk.StringVar(self.master)
        self.villain_pos_var.set("any")

        for t, val in self.positions:
            # rb = tk.Radiobutton(self.hero_pos, text=t, variable=self.hero_pos_var, value=m)
            self.hero_pos.add_radiobutton(label=t, value=val, variable=self.hero_pos_var)
            self.villain_pos.add_radiobutton(label=t, value=val, variable=self.villain_pos_var)

        self.villain_type = tk.Menu(self.menubar, tearoff=0)
        self.villain_type_var = tk.StringVar(self.master)
        self.villain_type_var.set("any")
        for v, val in self.villains:
            self.villain_type.add_radiobutton(label=v, value=val, variable=self.villain_type_var)

        self.table_size = tk.Menu(self.menubar, tearoff=0)
        self.table_size_var = tk.StringVar(self.master)
        self.table_size_var.set("any")
        for ta, val in self.tables:
            self.table_size.add_radiobutton(label=ta, value=val, variable=self.table_size_var)

        self.previous_actions = tk.Menu(self.menubar, tearoff=0)
        self.previous_actions_var = tk.StringVar(self.master)
        self.previous_actions_var.set("any")
        for p, val in self.previous_acts:
            self.previous_actions.add_radiobutton(label=p, value=val, variable=self.previous_actions_var)


        self.menubar.add_cascade(label="Hero Position", menu=self.hero_pos)
        self.menubar.add_cascade(label="Villain Position", menu=self.villain_pos)
        self.menubar.add_cascade(label="Villain Type", menu=self.villain_type)
        self.menubar.add_cascade(label="Table Size", menu=self.table_size)
        self.menubar.add_cascade(label="Previous Actions", menu=self.previous_actions)

        self.master.config(menu=self.menubar)


    def init_canvas(self):
        self.canvas = tk.Canvas(self.master, bg="white", width=13*self.box_size, height=13*self.box_size)
        # self.canvas.pack()
        self.canvas.pack(side=tk.RIGHT)


    def populate_listbox(self):
        filters = {}
        if self.hero_pos_var.get() != "any":
            filters["hero_pos"] = self.hero_pos_var.get()
        if self.villain_pos_var.get() != "any":
            filters["villain_pos"] = self.villain_pos_var.get()
        if self.villain_type_var.get() != "any":
            filter["villain_type"] = self.villain_type_var.get()
        if self.previous_actions_var.get() != "any":
            filter["previous_actions"] = self.previous_actions_var.get()
        if self.table_size_var.get() != "any":
            filter["table_size"] = self.table_size_var.get()

        self.ranges = json.loads(range_db.load_ranges(filters))

        for r in self.ranges:
            self.listbox.insert(tk.END, str(r[0]) + " | " + r[1] + " | " + r[4] + " | " + r[5] + " | " + r[6] + " | " + r[7] + " | " + r[8] + " | " + r[9])


    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.populate_listbox()


    def preview_range(self, event):
        try:
            active = self.ranges[self.listbox.index(tk.ACTIVE)]
            active_range = json.loads(active[2])
            colors = json.loads(active[3])
            for i in range(13):
                for j in range(13):
                    fill_color = colors[active_range[i][j]][1]
                    self.canvas.create_rectangle(i*self.box_size, j*self.box_size, (i+1)*self.box_size, (j+1)*self.box_size, fill=fill_color)
        except:
            return


    def return_range(self):
        return

    def load_new(self):
        rng = self.ranges[self.listbox.index(tk.ACTIVE)]
        action_color = json.loads(rng[3])
        actions = [i[0] for i in action_color]
        colors = [i[1] for i in action_color]
        kwargs = {
            "range_id": rng[0],
            "name": rng[1],
            "hand_range": json.loads(rng[2]),
            "actions": actions,
            "colors": colors,
            "hero_pos": rng[4],
            "villain_pos": rng[5],
            "villain_type": rng[6],
            "previous_actions": rng[7],
            "table_size": rng[8],
            "notes": rng[9]
        }
        return range_viewer.RangeViewer(tk.Tk(), **kwargs)

    def delete_range(self):
        if messagebox.askyesnocancel("Confirm", "Are you sure you want to delete this range?"):
            try:
                range_db.delete_range(self.ranges[self.listbox.index(tk.ACTIVE)][0])
                self.listbox.delete(self.listbox.index(tk.ACTIVE))
                del self.ranges[self.listbox.index(tk.ACTIVE)]
            except:
                return




if __name__ == '__main__':
    root = tk.Tk()
    app = RangeTable(master=root)
    app.mainloop()
