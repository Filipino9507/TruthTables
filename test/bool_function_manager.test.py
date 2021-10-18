import unittest
from bool_function.bool_function_manager import BoolFunctionManager

class FunctionManager_Test(unittest.TestCase):
    def save_function_test(self):
        test_filename = "functions_test"
        manager = BoolFunctionManager(test_filename)
        manager.save_function("func_1", "a&(b|c)=>a", ["a", "b", "c"])

        file_content = None
        with open(f"{manager.BASE_PATH}{test_filename}", "r+") as file:
            file_content = file.read()
            file.truncate(0)
        self.assertEqual(file_content, "func_1:a&(b|c)=>a:a,b,c\n")
