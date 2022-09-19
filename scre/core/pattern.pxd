

cdef class Pattern:
    cdef object _automaton
    cdef _fullmatch(self, str text, int flags, object state, int pos)