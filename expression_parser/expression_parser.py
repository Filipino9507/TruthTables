import re
from typing import Callable, List, Set, Tuple, Union
from enum import Enum, auto
from expression_parser.tree_node import TNExpression, TNOperatorAND, TNOperatorEquivalency, TNOperatorImplication, TNOperatorNOT, TNOperatorOR, TNValue, TNVariable, TreeNode


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

    TREE_BUILDING_STRATEGIES: List[Callable[[
        List[Token]], Union[List[Token], None]]] = []

    OPERATOR_PRIORITY: List[TokenType] = [
        TokenType.EQUIVALENCY,
        TokenType.IMPLICATION,
        TokenType.OR,
        TokenType.AND,
        TokenType.NOT,
    ]

    def __init__(self):
        self.TREE_BUILDING_STRATEGIES.append(self._try_build_expression)
        self.TREE_BUILDING_STRATEGIES.append(self._try_build_operator)
        self.TREE_BUILDING_STRATEGIES.append(self._try_build_leaves)
        self._variables = set()

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

    def _try_build_expression(self, token_list: List[Token]) -> Union[TreeNode, None]:
        if self._is_enclosed(token_list, lchar="(", rchar=")"):
            node = TNExpression(0, False)
            node.add_child(self._build_tree(token_list[1:len(token_list)-1]))
            return node
        if self._is_enclosed(token_list, lchar="[", rchar="]"):
            node = TNExpression(0, True)
            node.add_child(self._build_tree(token_list[1:len(token_list)-1]))
            return node
        return None

    def _try_build_operator(self, token_list: List[Token]) -> Union[TreeNode, None]:
        for operator in self.OPERATOR_PRIORITY:
            nest = 0
            for i, token in enumerate(token_list):
                tt = token.token_type
                if tt in (TokenType.LPAREN, TokenType.LBRACKET):
                    nest += 1
                elif tt in (TokenType.RPAREN, TokenType.RBRACKET):
                    nest -= 1
                elif tt == operator and nest == 0:
                    if tt == TokenType.AND:
                        node = TNOperatorAND(0)
                    elif tt == TokenType.OR:
                        node = TNOperatorOR(0)
                    elif tt == TokenType.NOT:
                        node = TNOperatorNOT(0)
                    elif tt == TokenType.IMPLICATION:
                        node = TNOperatorImplication(0)
                    elif tt == TokenType.EQUIVALENCY:
                        node = TNOperatorEquivalency(0)

                    if tt != TokenType.NOT:
                        node.add_child(self._build_tree(token_list[:i]))
                    elif i != 0:
                        raise Exception("Invalid NOT syntax.")
                    node.add_child(self._build_tree(token_list[i+1:]))
                    return node
        return None

    def _try_build_leaves(self, token_list: List[Token]) -> Union[TreeNode, None]:
        if len(token_list) != 0:
            last_token = token_list[0]
            if last_token.token_type == TokenType.VALUE:
                return TNValue(0, last_token.value)
            if last_token.token_type == TokenType.VARIABLE:
                self._variables.add(last_token.value)
                return TNVariable(0, last_token.value)

    def _build_tree(self, token_list: List[Token]) -> TreeNode:
        print("CURRENT TOKEN LIST: ", [t.value for t in token_list])

        for tree_building_strategy in self.TREE_BUILDING_STRATEGIES:
            result = tree_building_strategy(token_list)
            if result:
                return result

        raise Exception("Invalid syntax.")

    def parse(self, expression: str) -> Union[
        Tuple[TreeNode, Set[str], None],
        Tuple[None, None, Exception]
    ]:
        try:
            print("[TOKENIZING]")
            token_list = self._tokenize(expression)
            print("[PARSING]")
            self._variables.clear()
            tree = self._build_tree(token_list)
            print("[GENERATING_TABLE]")

            for t in token_list:
                print(f"TYPE: {t.token_type}, VALUE: {t.value}")
            print(tree)
            print(self._variables)

            return [tree, self._variables, None]
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return [None, None, e]
