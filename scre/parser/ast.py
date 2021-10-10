from typing import List
import cython

@cython.cclass
class ExpBase:
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpCharRange(ExpBase):
    def __init__(self, chars: List[ExpBase], positive: cython.bint) -> None:
        self._chars = chars
        self._positive = positive

@cython.cclass
class ExpChar(ExpBase):
    def __init__(self, c: cython.Py_UCS4) -> None:
        self._char = c

@cython.cclass
class ExpOr(ExpBase):
    def __init__(self, exprs: List[ExpBase]) -> None:
        self._exprs = exprs


@cython.cclass
class ExpSeq(ExpBase):
    def __init__(self, exprs: List[ExpBase]) -> None:
        self._exprs = exprs


@cython.cclass
class ExpLoop(ExpBase):
    def __init__(self, expr: ExpBase, loop: cython.Py_UCS4, lazy: cython.bint) -> None:
        self._expr = expr
        self._loop = loop
        self._lazy = lazy