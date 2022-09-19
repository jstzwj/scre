cdef class State:
    cdef public Py_UCS4 c
    cdef public bint virtual
    cdef public list outs
    cdef public list ins

cdef class Automaton:
    cdef list _states
    cdef int _start
    cdef int _end

    cdef set_start(self, int i)
    cdef set_end(self, int i)
    cdef add_virtual_element(self)
    cdef add_element(self, Py_UCS4 c)
    cdef connect(self, State f, State t)
