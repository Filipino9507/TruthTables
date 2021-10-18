import tkinter as tk

from gui.logic_table import LogicTable
from parser.expression_parser import ExpressionParser
from parser.table_generator import TableGenerator
from bool_function.bool_function_manager import BoolFunctionManager
from bool_function.bool_function import BoolFunction


class GUI(tk.Frame):
    def __init__(self, *, master, expression_parser: ExpressionParser, table_generator: TableGenerator, bool_function_manager: BoolFunctionManager):
        tk.Frame.__init__(self, master)
        self.master = master
        self.expression_parser = expression_parser
        self.table_generator = table_generator
        self.bool_function_manager = bool_function_manager
        self.pack()

        self.current_expression = ""
        self.current_variable_ls = []

        self.setup()

    def setup(self):
        self.setup_entry_expression()
        self.setup_button_generate_table()
        self.setup_button_save_function()
        self.setup_label_error_message()
        self.setup_logic_table()

    def setup_entry_expression(self):
        self.entry_expression_content = tk.StringVar()
        self.entry_expression_previous_value = ''
        self.entry_expression_has_changed = False

        def on_entry_expression_value_change(_):
            maxlen = 50
            value = self.entry_expression_content.get().strip()
            if self.entry_expression_previous_value != value and len(value) > maxlen:
                self.entry_expression_content.set(value[:maxlen])
                self.entry_expression_previous_value = value
            self.entry_expression_has_changed = True

        self.entry_expression = tk.Entry(
            self, width=50, borderwidth=3, relief="sunken",
            font=("PT Mono", 24), textvariable=self.entry_expression_content
        )
        self.entry_expression.bind(
            "<KeyRelease>", on_entry_expression_value_change)
        self.entry_expression.pack(side="top")

    def setup_button_generate_table(self):
        def on_button_generate_table_click():
            if not self.entry_expression_has_changed:
                return
            expr = self.entry_expression_content.get().strip()
            tree, variables, err = self.expression_parser.parse(expr)
            if err:
                self.label_error_message_content.set(str(err))
                return
            self.label_error_message_content.set("")
            content = self.table_generator.generate_table_content(
                tree, variables)
            self.entry_expression_has_changed = False
            self.logic_table.populate(content)
            self.current_variable_ls = variables

        self.button_generate_table = tk.Button(
            self, text="Generate Table", command=on_button_generate_table_click)
        self.button_generate_table.pack(side="top")

    def setup_button_save_function(self):
        def on_button_save_function():
            if len(self.entry_expression_content.get()) == 0:
                self.label_error_message_content.set(
                    "No expression to save as function.")
                return
            new_function = BoolFunction(
                "FUNCTION_NAME", self.entry_expression_content.get(), self.current_variable_ls)
            self.bool_function_manager.save(new_function)
        self.button_save_function = tk.Button(
            self, text="Save Last Function", command=on_button_save_function)
        self.button_save_function.pack(side="top")

    def setup_label_error_message(self):
        self.label_error_message_content = tk.StringVar()
        self.label_error_message = tk.Label(
            self, textvariable=self.label_error_message_content, fg="#f00")
        self.label_error_message.pack(side="top")

    def setup_logic_table(self):
        self.logic_table = LogicTable(self)
        self.logic_table.pack(side="bottom")
