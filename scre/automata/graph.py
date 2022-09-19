

from typing import List, Set
import cython

@cython.cclass
class State:
    def __init__(self) -> None:
        self.c: cython.Py_UCS4 = '\0'
        self.virtual: cython.bint = False
        self.outs: List[State] = list()
        self.ins: List[State] = list()

@cython.cclass
class Automaton:
    def __init__(self) -> None:
        self._states: List[State] = []
        self._start: cython.int = -1
        self._end: cython.int = -1

    @property
    def start(self):
        return self._states[self._start]
    
    @property
    def end(self):
        return self._states[self._end]
    
    def set_start(self, i: cython.int):
        self._start = i
    
    def set_end(self, i: cython.int):
        self._end = i

    def add_virtual_element(self):
        state = State()
        state.virtual = True
        self._states.append(state)
        return state

    def add_element(self, c: cython.Py_UCS4):
        state = State()
        state.c = c
        state.virtual = False
        self._states.append(state)
        return state
    
    def connect(self, f, t):
        f.outs.append(t)
        t.ins.append(f)

