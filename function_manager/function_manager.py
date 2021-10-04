from typing import List


class FunctionManager:

    # "[NAME]:[EXPRESSION]:[VARIABLES (comma separated)]"
    FUNCTION_FORMAT = "%s:%s:%s\n"
    BASE_PATH = "../data/"

    def __init__(self, filename: str):
        self._filename = filename

    def save_function(self, name: str, expression: str, variable_ls: List[str]) -> None:
        variables = ",".join(variable_ls)
        with open(f"{self.BASE_PATH}{self._filename}", "a") as file:
            file.write(self.FUNCTION_FORMAT % (name, expression, variables))

    def load_function(self, name: str) -> None:
        # Loads function with param name
        pass

    
