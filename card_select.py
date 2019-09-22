import tkinter as tk


class CardSelect:
    def __init__(self, master=None, *args, **kwargs):
        # if master is None:
        #     master = tk.Tk()
        #
        # self.frame = super().__init__(master)
        self.master = master

        self.top = tk.Toplevel(self.master)
        self.top.title("Select Cards")

        self.max_select = 5
        if "max_select" in kwargs:
            self.max_select = kwargs["max_select"]

        self.disallowed_cards = []
        if "disallowed_cards" in kwargs:
            self.disallowed_cards = kwargs["disallowed_cards"]

        self.cc_mode = True
        if "mode" in kwargs:
            self.cc_mode = kwargs["mode"]

        self.suits = ['s', 'c', 'h', 'd']
        self.unselected_colors = ["gray", "green", "red", "blue"]
        self.selected_colors = ["#34393b", "#015e1a", "#b80202", "#3333ff"]
        self.vals = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

        self.selected_cards = []

        self.box_size = 30

        self.initUI()

    def initUI(self):
        self.canvas = tk.Canvas(self.top, width=self.box_size*13, height=self.box_size*4)

        for v in range(13):
            for s in range(4):
                self.canvas.create_rectangle(v*self.box_size, s*self.box_size, (v+1)*self.box_size, (s+1)*self.box_size, fill=self.unselected_colors[s])
                self.canvas.create_text((v+0.5)*self.box_size, (s+0.5)*self.box_size, text=self.vals[v] + self.suits[s], fill="white")

        self.canvas.bind("<Button-1>", self.select_card)

        self.ok_button = tk.Button(self.top, text="OK", command=self.ok)
        self.cancel_button = tk.Button(self.top, text="Cancel", command=self.close)

        self.canvas.grid(row=0, column=0, columnspan=2)
        self.ok_button.grid(row=1, column=0)
        self.cancel_button.grid(row=1, column=1)

    def select_card(self, event):
        x = max(min(event.x // self.box_size, 12), 0)
        y = max(min(event.y // self.box_size, 3), 0)

        card = self.vals[x] + self.suits[y]
        if card in self.selected_cards:
            self.selected_cards.remove(card)
            self.canvas.create_rectangle(x*self.box_size, y*self.box_size, (x+1)*self.box_size, (y+1)*self.box_size, fill=self.unselected_colors[y])
            self.canvas.create_text((x+0.5)*self.box_size, (y+0.5)*self.box_size, text=card, fill="white")
        elif len(self.selected_cards) < self.max_select and card not in self.disallowed_cards:
            self.selected_cards.append(card)
            self.canvas.create_rectangle(x*self.box_size, y*self.box_size, (x+1)*self.box_size, (y+1)*self.box_size, fill=self.selected_colors[y])
            self.canvas.create_text((x+0.5)*self.box_size, (y+0.5)*self.box_size, text=card, fill="white")

    def ok(self, *args):
        if self.cc_mode:
            self.master.community_cards = self.selected_cards
        else:
            self.master.dead_cards = self.selected_cards
        self.close()
    def close(self, *args):
        self.master.focus_set()
        self.top.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = CardSelect(master=root)
    app.mainloop()
