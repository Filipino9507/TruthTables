from typing import List


class BoolFunction:
    def __init__(self, name: str, expression: str, variable_ls: List[str]):
        self.name = name
        self.expression = expression
        self.variable_ls = variable_ls
