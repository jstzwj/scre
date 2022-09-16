

cdef class OptionChar:
    cdef Py_UCS4 _char
    cdef bint _has_value

    cdef bint is_some(self)
    cdef bint is_null(self)

    cdef Py_UCS4 value(self)
    cdef Py_UCS4 value_or(self, Py_UCS4 opt)
