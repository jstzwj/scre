

from scre.core.pattern import Pattern
from scre.parser.parser import Parser

def search(pattern: str, text: str) -> Pattern:
    parser = Parser(pattern)
    ast = parser.parse()
    print(parser.diagnostic)