

cdef class ExpBase:
    pass

cdef class ExpRE(ExpBase):
    cdef list _exprs

cdef class ExpSimpleRE(ExpBase):
    cdef list _exprs

cdef class ExpBasicRE(ExpBase):
    pass

cdef class ExpElementaryRE(ExpBasicRE):
    pass

cdef class ExpSetItem(ExpBase):
    pass

cdef class ExpGroup(ExpElementaryRE):
    cdef str _group_type
    cdef object _expr

cdef class ExpChar(ExpElementaryRE):
    cdef Py_UCS4 _char

cdef class ItemChar(ExpSetItem):
    cdef Py_UCS4 _char

cdef class ItemCharRange(ExpSetItem):
    cdef list _chars
    cdef bint _positive

cdef class ExpLoop(ExpBasicRE):
    cdef ExpBase _expr
    cdef int _start
    cdef int _end
    cdef bint _lazy
