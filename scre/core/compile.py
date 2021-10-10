
from scre.core.pattern import Pattern
from scre.parser.parser import Parser

def compile(pattern: str, flags: int=0) -> Pattern:
    parser = Parser(pattern)
    ast = parser.parse()
    print(parser.diagnostic)