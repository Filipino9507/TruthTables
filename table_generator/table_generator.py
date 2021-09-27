from typing import List, Set
from expression_parser.tree_node import TreeNode


class TableGenerator:
    def __init__(self):
        pass

    def _get_value_combinations(
        self,
        current: List[bool],
        idx: int,
        variable_count: int
    ) -> List[List[bool]]:
        if idx == variable_count:
            return [current]

        value_combinations = []
        current[idx] = True
        value_combinations += self._get_value_combinations(
            current[:], idx + 1, variable_count)
        current[idx] = False
        value_combinations += self._get_value_combinations(
            current[:], idx + 1, variable_count)

        return value_combinations

    def generate_table_content(self, tree: TreeNode, variables: Set[str]) -> List[List[str]]:
        variable_ls = sorted(list(variables))
        variable_dict = {name: i for i, name in enumerate(variable_ls)}
        value_combinations = self._get_value_combinations(
            [None] * len(variable_ls), 0, len(variable_ls))

        # print(f"VALUE COMBINATIONS: {value_combinations}")
        # print(f"VARIABLE DICT: {variable_dict}")

        for value_combination in value_combinations:
            expression_values_dict = {}
            print(f"COMBINATION: {tree.get_value(variable_dict, value_combination, expression_values_dict)}")
            print(f"EXPRESSIONS: {expression_values_dict}")

        return []
