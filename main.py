import tkinter as tk

from const import WIN_WIDTH, WIN_HEIGHT


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.setup()

    def setup(self):
        self.setup_entry_expression_content()
        self.setup_button_generate_table()
        self.setup_button_save_function()

    def setup_entry_expression_content(self):
        self.entry_expression_content = tk.StringVar()
        self.entry_expression_previous_value = ''

        def on_entry_expression_value_change(_):
            maxlen = 50
            value = self.entry_expression_content.get().strip()
            if self.entry_expression_previous_value != value and len(value) > maxlen:
                self.entry_expression_content.set(value[:maxlen])
                self.entry_expression_previous_value = value

        self.entry_expression = tk.Entry(
            self, width=50, borderwidth=3, relief="sunken",
            font=("PT Mono", 24), textvariable=self.entry_expression_content
        )
        self.entry_expression.bind("<KeyRelease>", on_entry_expression_value_change)
        self.entry_expression.pack(side="top")

    def setup_button_generate_table(self):
        self.button_generate_table = tk.Button(self, text="Generate Table")
        self.button_generate_table.pack(side="top")

    def setup_button_save_function(self):
        self.button_save_function = tk.Button(self, text="Save Function")
        self.button_save_function.pack(side="bottom")


root = tk.Tk(className="Truth Tables")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.minsize(WIN_WIDTH, WIN_HEIGHT)
root.maxsize(WIN_WIDTH, WIN_HEIGHT)
gui = GUI(master=root)
gui.mainloop()
