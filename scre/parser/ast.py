from typing import List
import cython

@cython.cclass
class ExpBase:
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpRE(ExpBase):
    def __init__(self, exprs: List["ExpSimpleRE"]) -> None:
        self._exprs = exprs

@cython.cclass
class ExpSimpleRE(ExpBase):
    def __init__(self, exprs: List["ExpBasicRE"]) -> None:
        self._exprs = exprs

@cython.cclass
class ExpBasicRE(ExpBase):
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpElementaryRE(ExpBasicRE):
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpSetItem(ExpBase):
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpGroup(ExpElementaryRE):
    def __init__(self, group_type: str, expr: ExpRE) -> None:
        self._group_type = group_type
        self._expr = expr

@cython.cclass
class ExpAny(ExpElementaryRE):
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpEOS(ExpElementaryRE):
    def __init__(self) -> None:
        pass

@cython.cclass
class ExpSet(ExpElementaryRE):
    def __init__(self, positive: bool, items: List["ExpSetItem"]) -> None:
        self._positive = positive
        self._items = items

@cython.cclass
class ExpChar(ExpElementaryRE):
    def __init__(self, c: cython.Py_UCS4) -> None:
        self._char = c

@cython.cclass
class ItemChar(ExpSetItem):
    def __init__(self, c: cython.Py_UCS4) -> None:
        self._char = c

@cython.cclass
class ItemCharRange(ExpSetItem):
    def __init__(self, start: cython.Py_UCS4, end: cython.Py_UCS4) -> None:
        self._start = start
        self._end = end

@cython.cclass
class ExpLoop(ExpBasicRE):
    def __init__(self, expr: ExpElementaryRE, start: cython.int, end: cython.int, lazy: cython.bint) -> None:
        self._expr = expr
        self._start = start
        self._end = end
        self._lazy = lazy