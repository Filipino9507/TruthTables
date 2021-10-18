from typing import List, Generator
from bool_function.bool_function import BoolFunction


class BoolFunctionManager:

    # "[NAME]:[EXPRESSION]:[VARIABLES (comma separated)]"
    FUNCTION_FORMAT = "%s:%s:%s\n"
    BASE_PATH = "../data/"

    def __init__(self, filename: str):
        self._filename = filename

    def save(self, bool_function: BoolFunction) -> None:
        variables = ",".join(bool_function.variable_ls)
        with open(f"{self.BASE_PATH}{self._filename}", "a") as file:
            file.write(self.FUNCTION_FORMAT %
                       (bool_function.name, bool_function.expression, variables))

    def load_all(self) -> Generator[BoolFunction, None, None]:
        with open(f"{self.BASE_PATH}{self._filename}", "r") as file:
            repr = file.read()
            split_repr = repr.split("\n")
            for result_ln in split_repr:
                name, expression, variables = result_ln.split(":")
                variable_ls = variables.split(",")
                yield BoolFunction(name, expression, variable_ls)

    def load_by_name(self, name: str) -> Generator[BoolFunction, None, None]:
        for bool_function in self.load_all():
            if bool_function.name == name:
                yield bool_function
