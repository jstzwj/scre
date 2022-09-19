
cdef class Automaton:
    cdef list _states
    cdef int _start
    cdef int _end

cdef class State:
    cdef Py_UCS4 char
    cdef bint virtual
    cdef set outs
    cdef set ins