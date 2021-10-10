

cdef class OptionChar:
    cdef Py_UCS4 _char
    cdef bint _has_value

    cpdef bint is_some(self)
    cpdef bint is_null(self)