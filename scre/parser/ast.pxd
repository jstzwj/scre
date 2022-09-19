
cdef class ExpBase:
    cdef int kind

cdef class ExpRE(ExpBase):
    cdef public list exprs

cdef class ExpSimpleRE(ExpBase):
    cdef public list exprs

cdef class ExpGroup(ExpBase):
    cdef str _group_type
    cdef object _expr

cdef class ExpChar(ExpBase):
    cdef Py_UCS4 c

cdef class ItemChar(ExpBase):
    cdef Py_UCS4 c

cdef class ItemCharRange(ExpBase):
    cdef list _chars
    cdef bint _positive

cdef class ExpLoop(ExpBase):
    cdef ExpBase _expr
    cdef int _start
    cdef int _end
    cdef bint _lazy
