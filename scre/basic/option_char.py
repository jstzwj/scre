
import cython
@cython.cclass
class OptionChar:
    def __init__(self, c: cython.Py_UCS4, has_value: cython.bint):
        self._char: cython.Py_UCS4 = c
        self._has_value: cython.bint = has_value

    def is_some(self) -> cython.bint:
        return self._has_value
    
    def is_null(self) -> cython.bint:
        return not self._has_value

    def value(self) -> cython.Py_UCS4:
        return self._char

    def value_or(self, opt: cython.Py_UCS4) -> cython.Py_UCS4:
        if not self._has_value:
            return opt
        else:
            return self._char

    @staticmethod
    def Null() -> 'OptionChar':
        return OptionChar('\0', False)

    @staticmethod
    def Some(c: cython.Py_UCS4) -> 'OptionChar':
        return OptionChar(c, True)
