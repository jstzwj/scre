from scre.automata.graph cimport State

cdef class Pattern:
    cdef object _automaton
    cdef _fullmatch(self, str text, int flags, State state, int pos)