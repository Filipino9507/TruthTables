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
    def get_value(self) -> bool:
        pass

    def _get_error_here(self) -> str:
        return f"Invalid tree topology at node with ID {self._id}."

    def _get_representation(self, nest=0):
        representation = f"{nest * '|---'}{type(self).__name__}\n"
        for child in self._children:
            representation += child._get_representation(nest + 1)
        return representation
    
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

    def get_value(self) -> bool:
        self._check_validity()
        return self._children[0].get_value() and self._children[1].get_value()


class TNOperatorOR(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(self) -> bool:
        self._check_validity()
        return self._children[0].get_value() or self._children[1].get_value()


class TNOperatorNOT(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 1)

    def get_value(self) -> bool:
        self._check_validity()
        return not self._children[0].get_value()


class TNOperatorImplication(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(self) -> bool:
        self._check_validity()
        return not(self._children[0].get_value() and not self._children[1].get_value())


class TNOperatorEquivalency(TNOperator):
    def __init__(self, id: int):
        super().__init__(id, 2)

    def get_value(self) -> bool:
        self._check_validity()
        return self._children[0].get_value() == self._children[1].get_value()


class TNExpression(TreeNode):
    def __init__(self, id: int, to_register: bool):
        super().__init__(id)
        self._to_register = to_register

    def add_child(self, child: TreeNode) -> None:
        if len(self._children) == 0:
            super().add_child(child)
        else:
            raise Exception(
                f"{self._get_error_here()} Expressions can only have 1 child.")

    def get_value(self) -> bool:
        return self._children[0].get_value()


class TNVariable(TreeNode):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self._name = name

    def add_child(self, _: TreeNode) -> None:
        raise Exception(
            f"{self._get_error_here()} Variables cannot have children.")

    def get_value(self, variables: Dict[str, bool]) -> bool:
        return variables[self._name]


class TNValue(TreeNode):
    def __init__(self, id: int, value: bool):
        super().__init__(id)
        self._value = value

    def add_child(self, _: TreeNode) -> None:
        raise Exception(
            f"{self._get_error_here()} Values cannot have children.")

    def get_value(self) -> bool:
        return self._value
