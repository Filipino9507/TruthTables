from typing import List, Set
from parser.tree_node import TreeNode


class TableGenerator:
    def __init__(self):
        pass

    def _generate_value_combinations(
        self,
        current: List[bool],
        idx: int,
        variable_count: int
    ) -> List[List[bool]]:
        if idx == variable_count:
            return [current]

        value_combinations = []
        current[idx] = True
        value_combinations += self._generate_value_combinations(
            current[:], idx + 1, variable_count)
        current[idx] = False
        value_combinations += self._generate_value_combinations(
            current[:], idx + 1, variable_count)

        return value_combinations

    def generate_table_content(self, tree: TreeNode, variables: Set[str]) -> List[List[str]]:
        variable_ls = sorted(list(variables), key=str.casefold)
        variable_dict = {name: i for i, name in enumerate(variable_ls)}
        value_combinations = self._generate_value_combinations(
            [None] * len(variable_ls), 0, len(variable_ls))
        expression_names_ls = tree.get_expression_names()

        table_content = [variable_ls + expression_names_ls + ["V"]]
        for value_combination in value_combinations:
            expression_values_dict = {}
            result_value = tree.get_value(
                variable_dict, value_combination, expression_values_dict)

            table_content.append(
                [int(x) for x in value_combination] +
                [expression_values_dict[expression_name]
                    for expression_name in expression_names_ls] +
                [result_value]
            )

        return table_content
