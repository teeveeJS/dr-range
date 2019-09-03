import tkinter as tk
from tkinter import simpledialog

from decimal import Decimal


import note_dialog
import range_db
import range_viewer
import range_table

from utils import coord_to_hand, count_combos


class RangeViewer(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        if master is None:
            master = tk.Tk()

        super().__init__(master)
        self.master = master

        if "range_id" in kwargs:
            self.range_id = kwargs["range_id"]
        else:
            self.range_id = -1

        if "name" in kwargs:
            self.range_name = kwargs["name"]
        else:
            self.range_name = "Unnamed Range"
        self.master.title(self.range_name)


        #idk pick suitable colors
        self.colors = ["lightgreen", "red", "lightblue", "#1e90ff", "orange", "lightgray", "violet", "white"]

        self.color_buttons = []
        self.colors_labels = []

        if "colors" in kwargs:
            self.colors = kwargs["colors"]

        self.active_color = self.colors[0]


        if "actions" in kwargs:
            self.action_names = kwargs["actions"]
        else:
            self.action_names = ["Action " + str(i) for i in range(len(self.colors))]



        self.box_size = 30
        self.previous_square = [] #store i, j of the previous square

        self.hand_range = []
        self.counts = []

        self.dead_cards = []

        if "hand_range" in kwargs:
            self.hand_range = kwargs["hand_range"]
        else:
            self.init_range()

        self.init_counts()



        self.hero_pos_var = tk.StringVar(self.master)
        if "hero_pos" in kwargs:
            self.hero_pos_var.set(kwargs["hero_pos"])
        else:
            self.hero_pos_var.set("any")

        self.villain_pos_var = tk.StringVar(self.master)
        if "villain_pos" in kwargs:
            self.villain_pos_var.set(kwargs["villain_pos"])
        else:
            self.villain_pos_var.set("any")

        self.villain_type_var = tk.StringVar(self.master)
        if "villain_type" in kwargs:
            self.villain_type_var.set(kwargs["villain_type"])
        else:
            self.villain_type_var.set("any")

        self.table_size_var = tk.StringVar(self.master)
        if "table_size" in kwargs:
            self.table_size_var.set(kwargs["table_size"])
        else:
            self.table_size_var.set("any")

        self.previous_actions_var = tk.StringVar(self.master)
        if "previous_actions" in kwargs:
            self.previous_actions_var.set(kwargs["previous_actions"])
        else:
            self.previous_actions_var.set("any")

        self.notes = ""
        if "notes" in kwargs:
            self.notes = kwargs["notes"]






        self.unsaved_changes = False



        self.initUI()


    def initUI(self):
        self.draw_full_range()

        self.init_color_buttons()
        self.init_count_labels()
        self.update_count_labels()

        self.create_menubar()


    def draw_full_range(self):
        self.canvas = tk.Canvas(self.master, bg=self.colors[-1], width=13*self.box_size, height=13*self.box_size)
        self.canvas.grid(row=0, column=0, rowspan=100)

        for i in range(13):
            for j in range(13):
                fill_color = self.colors[self.hand_range[i][j]]
                self.canvas.create_rectangle(i*self.box_size, j*self.box_size, (i+1)*self.box_size, (j+1)*self.box_size, fill=fill_color)
                self.canvas.create_text((i+0.5)*self.box_size, (j+0.5)*self.box_size, text=coord_to_hand(i, j))


        self.canvas.bind('<Button-1>', self.start_select)
        self.canvas.bind('<B1-Motion>', self.active_select)
        self.canvas.bind('<ButtonRelease-1>', self.finish_select)

    def init_color_buttons(self):
        self.color_buttons = [None]*len(self.colors)
        for i in range(len(self.colors)):
            self.color_buttons[i] = tk.Button(self.master, text=self.action_names[i], bg=self.colors[i])
            self.color_buttons[i].bind('<Button-1>', self.activate_color)
            self.color_buttons[i].bind('<Button-3>', self.change_action_name)
            self.color_buttons[i].grid(row=i, column=1, padx=2, pady=2)

    def init_count_labels(self):
        self.color_labels = [None]*len(self.colors)
        for i in range(len(self.colors)):
            self.color_labels[i] = tk.Label(self.master, text='', width=16)
            self.color_labels[i].grid(row=i, column=2, pady=2)

    def create_menubar(self):
        self.menubar = tk.Menu(self.master)

        self.file_opts = tk.Menu(self.menubar, tearoff=0)
        self.file_opts.add_command(label="New Range", command=self.new_range)
        self.file_opts.add_command(label="Clear Range", command=self.clear_range)
        self.file_opts.add_command(label="Browse Ranges", command=self.browse_ranges)
        self.file_opts.add_command(label="Save Range", command=self.save_range)
        self.file_opts.add_command(label="Export Range", command=self.export_range)
        self.file_opts.add_command(label="Export as PNG", command=self.export_png)
        self.menubar.add_cascade(label="File", menu=self.file_opts)

        self.range_opts = tk.Menu(self.menubar, tearoff=0)
        self.range_opts.add_command(label="Edit Name", command=self.name_range)

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

        self.hero_pos = tk.Menu(self.range_opts, tearoff=0)
        self.villain_pos = tk.Menu(self.range_opts, tearoff=0)

        for t, val in self.positions:
            # rb = tk.Radiobutton(self.hero_pos, text=t, variable=self.hero_pos_var, value=m)
            self.hero_pos.add_radiobutton(label=t, value=val, variable=self.hero_pos_var)
            self.villain_pos.add_radiobutton(label=t, value=val, variable=self.villain_pos_var)

        self.villain_type = tk.Menu(self.range_opts, tearoff=0)
        for v, val in self.villains:
            self.villain_type.add_radiobutton(label=v, value=val, variable=self.villain_type_var)

        self.previous_actions = tk.Menu(self.range_opts, tearoff=0)
        for p, val in self.previous_acts:
            self.previous_actions.add_radiobutton(label=p, value=val, variable=self.previous_actions_var)

        self.table_size = tk.Menu(self.range_opts, tearoff=0)
        for ta, val in self.tables:
            self.table_size.add_radiobutton(label=ta, value=val, variable=self.table_size_var)


        self.range_opts.add_cascade(label="Hero Position", menu=self.hero_pos)
        self.range_opts.add_cascade(label="Villain Position", menu=self.villain_pos)
        self.range_opts.add_cascade(label="Villain Type", menu=self.villain_type)
        self.range_opts.add_cascade(label="Previous Actions", menu=self.previous_actions)
        self.range_opts.add_cascade(label="Table Size", menu=self.table_size)
        self.range_opts.add_command(label="Add Notes", command=self.add_notes)
        self.range_opts.add_command(label="Add Tags", command=self.add_tags)


        self.menubar.add_cascade(label="Options", menu=self.range_opts)

        self.master.config(menu=self.menubar)


    def init_range(self):
        self.hand_range = []
        for _ in range(13):
            self.hand_range.append([len(self.colors)-1]*13)

    def init_counts(self):
        self.counts = [0]*len(self.colors)
        for i in range(13):
            for j in range(13):
                self.counts[self.hand_range[i][j]] += count_combos(i, j)

    def update_counts(self, i, j, old_color, new_color):
        count = count_combos(i, j)
        self.counts[old_color] -= count
        self.counts[new_color] += count

    def update_count_labels(self):
        for i in range(len(self.colors)):
            self.color_labels[i].config(text=str(self.counts[i]) + "/1326 (" + str(Decimal(100*self.counts[i] / 1326).quantize(Decimal('1.000'))) + "%)")


    def get_square(self, x, y):
        return [max(min(x // self.box_size, 12), 0), max(min(y // self.box_size, 12), 0)]

    def update_color(self, i, j):
        clr = self.active_color
        old_color_ind = self.hand_range[i][j]
        new_color_ind = self.colors.index(self.active_color)
        if old_color_ind == new_color_ind:
            clr = self.colors[-1]
            new_color_ind = len(self.colors)-1

        self.canvas.create_rectangle(i*self.box_size, j*self.box_size, (i+1)*self.box_size, (j+1)*self.box_size, fill=clr)
        self.canvas.create_text((i+0.5)*self.box_size, (j+0.5)*self.box_size, text=coord_to_hand(i, j))

        self.hand_range[i][j] = new_color_ind
        self.update_counts(i, j, old_color_ind, new_color_ind)
        self.update_count_labels()

    def start_select(self, event):
        curr_sq = self.get_square(event.x, event.y)
        # self.current_select.append(curr_sq)
        self.update_color(*curr_sq)
        self.previous_square = curr_sq

    def active_select(self, event):
        curr_sq = self.get_square(event.x, event.y)
        if self.previous_square == [] or curr_sq[0] != self.previous_square[0] or curr_sq[1] != self.previous_square[1]:
            self.update_color(*curr_sq)
            self.previous_square = curr_sq

    def finish_select(self, event):
        self.previous_square = []


    def activate_color(self, event):
        self.active_color = event.widget.config('background')[-1]
        # print("Active: " + self.active_color)

    def change_action_name(self, event):
        new_action_name = simpledialog.askstring("Input", "Rename the action", parent=self.master)
        if new_action_name != "" and not new_action_name is None:
            event.widget.configure(text=new_action_name)


    def new_range(self):
        # same as clear_range but prompt to save any unsaved changes

        # ...
        self.clear_range()
        self.range_id = -1

    def clear_range(self):
        self.init_range()
        self.init_counts()
        self.draw_full_range()
        self.update_count_labels()

    def browse_ranges(self):
        br = range_table.RangeTable(tk.Tk())
        return

    def save_range(self):
        actions = []
        hr = self.hand_range.copy()
        index_map = {}
        for i in range(len(self.colors)):
            if self.counts[i] != 0:
                index_map[i] = len(actions)
                actions.append([self.color_buttons[i]['text'], self.colors[i]])

        for k in range(13):
            for l in range(13):
                hr[k][l] = index_map[hr[k][l]]

        range_db.save_range(self.range_name, hr, actions, self.hero_pos_var.get(),
            self.villain_pos_var.get(), self.villain_type_var.get(), self.previous_actions_var.get(),
            self.table_size_var.get(), self.notes)

    def export_range(self):
        return

    def export_png(self):
        # import io
        # from PIL import Image
        #
        # ps = self.canvas.postscript(colormode="color")
        # img = Image.open(io.BytesIO(ps.encode('utf-8')))
        # img.save(self.range_name + '.png')

        return


    def name_range(self):
        new_name = simpledialog.askstring("Input", "Rename Your Range:", parent=self.master)
        if new_name != "" and not new_name is None:
            self.range_name = new_name
            self.master.title(new_name)

    def add_notes(self):
        nd = note_dialog.NoteDialog(self, self.notes)
        # self.master.wait_window(nd.top)
        return
    def add_tags(self):
        return



    def _print_range(self):
        for i in range(13):
            s = ''
            for j in range(13):
                s += coord_to_hand(j, i) + "[" + str(self.hand_range[i][j]) + "] "
            print(s)
