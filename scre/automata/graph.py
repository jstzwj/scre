

from typing import List
import cython

@cython.cclass
class State:
    def __init__(self) -> None:
        pass

@cython.cclass
class Transition:
    def __init__(self) -> None:
        pass

@cython.cclass
class Automaton:
    def __init__(self) -> None:
        self.states: List[State] = []
        self.transitions: List[Transition] = []