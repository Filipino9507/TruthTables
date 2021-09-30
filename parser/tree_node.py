from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


class TreeNode(ABC):
    def __init__(self, id: int):
        self._id = id
        self._children: List[TreeNode] = []

    def add_child(self, child: TreeNode) -> None:
        self._children.append(child)

    @abstractmethod
    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        pass

    def _get_error_here(self) -> str:
        return f"Invalid tree topology at node with ID {self._id}."

    def _get_representation(self, nest=0):
        representation = f"{nest * '|---'}{type(self).__name__}\n"
        for child in self._children:
            representation += child._get_representation(nest + 1)
        return representation

    def get_expression_names(self) -> List[str]:
        expression_names = []
        for child in self._children:
            expression_names += child.get_expression_names()
        return expression_names

    def __repr__(self):
        return self._get_representation()


class TNOperator(TreeNode):
    def __init__(self, id: int, operand_count: int):
        super().__init__(id)
        self._operand_count = operand_count

    def _check_validity(self):
        if len(self._children) != self._operand_count:
            raise Exception(
                f"Invalid tree topology at node with ID {self._id}.")

    def add_child(self, child: TreeNode) -> None:
        if len(self._children) < self._operand_count:
            super().add_child(child)
        else:
            raise Exception(
                f"{self._get_error_here()} Operand count at max.")


class TNOperatorAND(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        self._check_validity()
        lvalue = self._children[0].get_value(variable_dict, value_combination,
                                             expression_values_dict)
        rvalue = self._children[1].get_value(variable_dict,
                                             value_combination, expression_values_dict)
        return lvalue and rvalue


class TNOperatorOR(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        self._check_validity()
        lvalue = self._children[0].get_value(variable_dict, value_combination,
                                             expression_values_dict)
        rvalue = self._children[1].get_value(variable_dict,
                                             value_combination, expression_values_dict)
        return lvalue or rvalue


class TNOperatorNOT(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 1)

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        self._check_validity()
        return not self._children[0].get_value(variable_dict, value_combination,
                                               expression_values_dict)


class TNOperatorImplication(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        self._check_validity()
        lvalue = self._children[0].get_value(variable_dict, value_combination,
                                             expression_values_dict)
        rvalue = self._children[1].get_value(variable_dict,
                                             value_combination, expression_values_dict)
        return not(lvalue and not rvalue)


class TNOperatorEquivalency(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:
        self._check_validity()
        lvalue = self._children[0].get_value(variable_dict, value_combination,
                                             expression_values_dict)
        rvalue = self._children[1].get_value(variable_dict,
                                             value_combination, expression_values_dict)
        return lvalue == rvalue


class TNExpression(TreeNode):
    def __init__(self, id: int, to_register: bool, table_repr: str = ""):
        super().__init__(id)
        self._to_register = to_register
        self._table_repr = table_repr[1:-1] \
            .strip().replace("[", "(").replace("]", ")")

    def add_child(self, child: TreeNode) -> None:
        if len(self._children) == 0:
            super().add_child(child)
        else:
            raise Exception(
                f"{self._get_error_here()} Expressions can only have 1 child.")

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        expression_values_dict: Dict[str, bool]
    ) -> bool:

        value = self._children[0].get_value(variable_dict, value_combination,
                                            expression_values_dict)
        if self._to_register:
            expression_values_dict[self._table_repr] = value
        return value

    def get_expression_names(self) -> List[str]:
        expression_names = super().get_expression_names()
        if self._to_register:
            return expression_names + [self._table_repr]
        return expression_names


class TNVariable(TreeNode):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self._name = name

    def add_child(self, _: TreeNode) -> None:
        raise Exception(
            f"{self._get_error_here()} Variables cannot have children.")

    def get_value(
        self,
        variable_dict: Dict[str, int],
        value_combination: List[bool],
        _: Dict[str, bool]
    ) -> bool:
        return value_combination[variable_dict[self._name]]

    def get_expression_names(self) -> List[str]:
        return []


class TNValue(TreeNode):
    def __init__(self, id: int, value: bool):
        super().__init__(id)
        self._value = value

    def add_child(self, _: TreeNode) -> None:
        raise Exception(
            f"{self._get_error_here()} Values cannot have children.")

    def get_value(
        self,
        _: Dict[str, int],
        __: List[bool],
        ___: Dict[str, bool]
    ) -> bool:
        return self._value

    def get_expression_names(self) -> List[str]:
        return []
