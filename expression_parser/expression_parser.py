import re
from typing import List, Tuple, Union
from enum import Enum, auto
from expression_parser.tree_node import TNExpression, TNOperator, TNOperatorAND, TNOperatorEquivalency, TNOperatorImplication, TNOperatorNOT, TNOperatorOR, TNValue, TNVariable, TreeNode


class TokenType(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    IMPLICATION = auto()
    EQUIVALENCY = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    VALUE = auto()
    VARIABLE = auto()


class Token:
    def __init__(self, value: str, token_type: TokenType):
        if token_type == TokenType.VALUE:
            value = str(int(value))
        self.value = value
        self.token_type = token_type


class ExpressionParser:

    TOKEN_REPRESENTATIONS: List[Tuple[re.Pattern, TokenType]] = [
        (re.compile("\&"), TokenType.AND),
        (re.compile("\|"), TokenType.OR),
        (re.compile("!"), TokenType.NOT),
        (re.compile("=>"), TokenType.IMPLICATION),
        (re.compile("<=>"), TokenType.EQUIVALENCY),
        (re.compile("\("), TokenType.LPAREN),
        (re.compile("\)"), TokenType.RPAREN),
        (re.compile("\["), TokenType.LBRACKET),
        (re.compile("\]"), TokenType.RBRACKET),
        (re.compile("[01]"), TokenType.VALUE),
        (re.compile("[a-zA-Z]+"), TokenType.VARIABLE)
    ]

    OPERATOR_PRIORITY: List[TokenType] = [
        TokenType.EQUIVALENCY,
        TokenType.IMPLICATION,
        TokenType.OR,
        TokenType.AND,
        TokenType.NOT,
    ]

    def __init__(self):
        pass

    def _tokenize(self, expression: str) -> List[Token]:
        token_list = []
        expression = "".join(expression.split())
        while len(expression) > 0:
            for token_repr, token_type in self.TOKEN_REPRESENTATIONS:
                match = re.match(token_repr, expression)
                if match:
                    token = Token(expression[:match.end()], token_type)
                    token_list.append(token)
                    expression = expression[match.end():]
                    break
            else:
                raise Exception(
                    f"Invalid symbol at: {expression[:min(5, len(expression))]}")
        return token_list

    def _is_enclosed(self, token_list: List[Token], *, lchar: str, rchar: str) -> bool:
        length = len(token_list)
        if length == 0:
            return False
        if token_list[0].value != lchar or token_list[length-1].value != rchar:
            return False
        nest = 0
        for i, token in enumerate(token_list):
            if token.value == lchar:
                nest += 1
            elif token.value == rchar:
                nest -= 1
            if nest == 0 and i != length-1:
                return False
        return True
            

    def _build_tree(self, token_list: List[Token]) -> TreeNode:
        # print("CURRENT TOKEN LIST: ", [t.value for t in token_list])

        if self._is_enclosed(token_list, lchar="(", rchar=")"):
            node = TNExpression(0, False)
            node.add_child(self._build_tree(token_list[1:len(token_list)-1]))
            return node
        if self._is_enclosed(token_list, lchar="[", rchar="]"):
            node = TNExpression(0, True)
            node.add_child(self._build_tree(token_list[1:len(token_list)-1]))
            return node

        for operator in self.OPERATOR_PRIORITY:
            for i, token in enumerate(token_list):
                if token.token_type == operator:
                    if token.token_type == TokenType.AND:
                        node = TNOperatorAND(0)
                    elif token.token_type == TokenType.OR:
                        node = TNOperatorOR(0)
                    elif token.token_type == TokenType.NOT:
                        node = TNOperatorNOT(0)
                    elif token.token_type == TokenType.IMPLICATION:
                        node = TNOperatorImplication(0)
                    elif token.token_type == TokenType.EQUIVALENCY:
                        node = TNOperatorEquivalency(0)
                    node.add_child(self._build_tree(token_list[:i]))
                    node.add_child(self._build_tree(token_list[i+1:]))
                    return node

        if len(token_list) != 0:
            last_token = token_list[0]
            if last_token.token_type == TokenType.VALUE:
                return TNValue(0, last_token.value)
            if last_token.token_type == TokenType.VARIABLE:
                return TNVariable(0, last_token.value)

        raise Exception("Invalid syntax.")

    def parse(self, expression: str) -> None:
        token_list = self._tokenize(expression)

        for t in token_list:
            print(f"TYPE: {t.token_type}, VALUE: {t.value}")

        tree = self._build_tree(token_list)

        print(tree)
