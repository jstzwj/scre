

cdef class ExpBase:
    pass

cdef class ExpCharRange(ExpBase):
    cdef list _chars
    cdef bint _positive

cdef class ExpChar(ExpBase):
    cdef Py_UCS4 _char

cdef class ExpOr(ExpBase):
    cdef list _exprs

cdef class ExpSeq(ExpBase):
    cdef list _exprs

cdef class ExpLoop(ExpBase):
    cdef ExpBase _expr
    cdef Py_UCS4 _loop
    cdef bint _lazy