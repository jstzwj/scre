

from typing import List
import cython

@cython.cclass
class State:
    def __init__(self) -> None:
        self.outs: List[Transition] = []
        self.ins: List[Transition] = []

@cython.cclass
class Transition:
    def __init__(self) -> None:
        pass

@cython.cclass
class Automaton:
    def __init__(self) -> None:
        self.states: List[State] = []
        self.transitions: List[Transition] = []