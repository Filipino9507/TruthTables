import re
from typing import List
from enum import Enum, auto
from expression_parser.tree_node import TNOperatorAND, TNOperatorEquivalency, TNOperatorImplication, TNOperatorNOT, TNOperatorOR, TNValue, TNVariable

class Token(Enum):
    AND = auto(), OR = auto(), NOT = auto(), IMPLICATION = auto(), EQUIVALENCY = auto(),
    LPAREN = auto(), RPAREN = auto(), LBRACKET = auto(), RBRACKET = auto(),
    VALUE = auto(), VARIABLE = auto()

class ExpressionParser:

    TOKEN_REPRESENTATIONS = [
        [re.compile("\&"), Token.AND],    
        [re.compile("\|"), Token.OR],
        [re.compile("!"), Token.NOT],
        [re.compile("=>"), Token.IMPLICATION],
        [re.compile("<=>"), Token.EQUIVALENCY],
        [re.compile("\("), Token.LPAREN],
        [re.compile("\)"), Token.RPAREN],
        [re.compile("\["), Token.LBRACKET],
        [re.compile("\]"), Token.RBRACKET],
        [re.compile("[01]"), Token.VALUE],
        [re.compile("[a-zA-Z]+"), Token.VARIABLE]
    ]

    def __init__(self):
        pass

    def _tokenize(self, expression: str) -> List[Token]:
        token_list = []
        expression = "".join(expression.split())
        while len(expression) > 0:
            for token_repr in self.TOKEN_REPRESENTATIONS:
                match = re.match(token_repr, expression)
                if match:
                    token_list.append(expression[:match.end()])
                    expression = expression[match.end():]
                    break
            else:
                raise Exception(
                    f"Invalid symbol at: {expression[:min(5, len(expression))]}")
        return token_list

    def parse(self, expression: str) -> None:
        token_list = self._tokenize(expression)
        print(token_list)