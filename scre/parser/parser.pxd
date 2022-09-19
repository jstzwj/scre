
from scre.basic.diagnostic cimport Diagnostic
from scre.basic.option_char cimport OptionChar

cdef class CharIterator:
    cdef str _source
    cdef int _len
    cdef int _index
    cdef Py_UCS4 next(self)
    cdef int advance_by(self, int n)
    cdef Py_UCS4 nth(self, int n)
    cdef Py_UCS4 look_nth(self, int n)

cdef class Parser:
    cdef CharIterator _chars
    cdef Diagnostic _diagnostic
    cdef list _cursor_stack

    cdef CharIterator chars(self)
    cdef Py_UCS4 nth_char(self, n: cython.int)
    cdef Py_UCS4 first(self)
    cdef Py_UCS4 second(self)
    cdef bint is_eof(self)
    cdef push_cursor(self)
    cdef pop_cursor(self)
    cdef drop_cursor(self)
    cdef Py_UCS4 bump(self)

    cpdef parse(self)
    cdef parse_union(self)
    cdef parse_concatenation(self)
    cdef parse_basic(self)
    cdef parse_elementary(self)
    cdef parse_char(self)
    cdef parse_loop(self)
    