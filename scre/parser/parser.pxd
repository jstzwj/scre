
from scre.basic.diagnostic cimport Diagnostic
from scre.basic.option_char cimport OptionChar

cdef class CharIterator:
    cdef str _source
    cdef int _index
    cdef OptionChar next(self)
    cdef int advance_by(self, int n)
    cpdef OptionChar nth(self, int n)

cdef class Parser:
    cdef str _source
    cdef CharIterator _chars
    cdef Diagnostic _diagnostic
    cdef list _cursor_stack

    cdef CharIterator chars(self)
    cdef OptionChar nth_char(self, n: cython.int)
    cdef OptionChar first(self)
    cdef OptionChar second(self)
    cdef bint is_eof(self)
    cdef push_cursor(self)
    cdef pop_cursor(self)
    cdef drop_cursor(self)
    cdef OptionChar bump(self)

    cpdef parse(self)