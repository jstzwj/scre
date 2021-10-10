from scre.basic.source cimport SourceLocation

cdef enum Severity:
    Ignored = 1
    Note = 2
    Warning = 3
    Error = 4
    Fatal = 5


cdef class DiagnosticMessage:
    cdef int _severity
    cdef str _message
    cdef SourceLocation _location

cdef class Diagnostic:
    cdef list messages
    cpdef add(self, DiagnosticMessage diagnostic_message)
    cpdef error(self, str message, SourceLocation location)
    cpdef clear(self)
