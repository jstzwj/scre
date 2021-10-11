from scre.core.pattern import Pattern
from scre.parser.parser import Parser

class Pattern:
    def __init__(self) -> None:
        pass

    def search(self, pattern: str, text: str) -> Pattern:
        parser = Parser(pattern)
        ast = parser.parse()
        print(parser.diagnostic)