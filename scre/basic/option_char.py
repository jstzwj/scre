
import cython
@cython.cclass
class OptionChar:
    def __init__(self, c: str = None):
        self._char: cython.Py_UCS4 = '\0'
        self._has_value: cython.bint = False
        if c is not None:
            self._char: cython.Py_UCS4 = c
            self._has_value: cython.bint = True

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
        return OptionChar(None)

    @staticmethod
    def Some(c: str) -> 'OptionChar':
        return OptionChar(c)
