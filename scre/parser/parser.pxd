
from scre.basic.diagnostic cimport Diagnostic
from scre.basic.option_char cimport OptionChar

cdef class CharIterator:
    cdef str _source
    cdef int _index
    cdef OptionChar next(self)
    cdef int advance_by(self, int n)
    cdef OptionChar nth(self, int n)
    cdef OptionChar look_nth(self, int n)

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
    cdef parse_union(self)
    cdef parse_concatenation(self)
    cdef parse_basic(self)
    cdef parse_elementary(self)
    cdef parse_char(self)
    cdef parse_loop(self)
    