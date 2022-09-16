from scre.automata.graph import Automaton
from scre.parser.parser import Parser

class Pattern(object):
    def __init__(self, automaton: Automaton) -> None:
        self._automaton = automaton

    def match(self, text: str, flags: int) -> bool:
        return False

    def search(self, text: str) -> "str":
        return None