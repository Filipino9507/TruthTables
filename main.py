import tkinter as tk
from const import WIN_WIDTH, WIN_HEIGHT
from gui.gui import GUI
from parser.expression_parser import ExpressionParser
from parser.table_generator import TableGenerator
from bool_function.bool_function_manager import BoolFunctionManager


def main():
    root = tk.Tk(className="truthtables")
    root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    root.minsize(WIN_WIDTH, WIN_HEIGHT)
    root.maxsize(WIN_WIDTH, WIN_HEIGHT)

    expression_parser = ExpressionParser()
    table_generator = TableGenerator()
    bool_function_manager = BoolFunctionManager("functions")

    gui = GUI(master=root, expression_parser=expression_parser,
              table_generator=table_generator, bool_function_manager=bool_function_manager)
    gui.mainloop()


if __name__ == "__main__":
    main()
