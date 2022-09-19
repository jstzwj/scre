import cython
from scre.automata.graph import Automaton, State
from scre.parser.parser import Parser

@cython.cclass
class Pattern:
    def __init__(self, automaton: Automaton) -> None:
        self._automaton = automaton

    def match(self, text: str, flags: int) -> bool:
        return False
    
    def _fullmatch(self, text, flags: cython.int, state, pos: cython.int) -> bool:
        text_length: cython.int = len(text)
        while pos < text_length:
            if len(state.outs) == 1:
                n = state.outs[0]
                if n.c == text[pos]:
                    state = n
                    pos += 1
                else:
                    return False
            else:
                for n in state.outs:
                    if self._fullmatch(text, flags, n, pos + 1):
                        return True
        
        return True

    def fullmatch(self, text: str, flags: int = 0) -> bool:
        return self._fullmatch(text, flags, self._automaton.start, 0)

    def search(self, text: str) -> "str":
        return None