

from typing import List, Set
import cython

@cython.cclass
class State:
    def __init__(self) -> None:
        self.char: cython.Py_UCS4 = '\0'
        self.virtual: cython.bint = False
        self.outs: Set[State] = set()
        self.ins: Set[State] = set()

@cython.cclass
class Automaton:
    def __init__(self) -> None:
        self._states: List[State] = []
        self.add_virtual_element()
        self._start: cython.int = 0
        self.add_virtual_element()
        self._end: cython.int = 1
        self.connect(self.start, self.end)

    @property
    def start(self):
        return self._states[self._start]
    
    @property
    def end(self):
        return self._states[self._end]

    def add_virtual_element(self):
        state = State()
        state.virtual = True
        self._states.append(state)
        return state

    def add_element(self, c: cython.Py_UCS4):
        state = State()
        state.char = c
        state.virtual = False
        self._states.append(state)
        return state
    
    def connect(self, f: State, t: State):
        f.outs.add(t)
        t.ins.add(f)



def join_automaton(lhs: Automaton, rhs: Automaton):
    ret = Automaton()
    ret._states.clear()
    ret._states.append(lhs.start)
    ret._states.append(rhs.end)
    ret._states.extend([s for i, s in enumerate(lhs._states) if i != lhs._start and i != lhs._end])
    ret._states.extend([s for i, s in enumerate(rhs._states) if i != rhs._start and i != rhs._end])

    for lhs_end in lhs.end.ins:
        lhs_end.outs.remove(lhs.end)
        
        for rhs_start in rhs.start.outs:
            lhs_end.outs.add(rhs_start)
            rhs_start.ins.remove(rhs.start)
            rhs_start.ins.add(lhs_end)

    ret._start = 0
    ret._end = 1
    return ret

def union_automaton(lhs: Automaton, rhs: Automaton):
    ret = Automaton()
    ret._states.extend(lhs._states[2:])
    ret._states.extend(rhs._states[2:])

    ret.start.outs.update(lhs.start.outs)
    ret.start.outs.update(rhs.start.outs)
    ret.end.ins.update(lhs.end.ins)
    ret.end.ins.update(rhs.end.ins)
    return ret


