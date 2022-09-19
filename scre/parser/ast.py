from typing import List, Union
import cython

@cython.cclass
class ExpKind:
    KindExpBase = 0
    KindExpRE = 1
    KindExpSimpleRE = 2
    KindExpBasicRE = 3
    KindExpElementaryRE = 4
    KindExpSetItem = 5
    KindExpGroup = 6
    KindExpAny = 7
    KindExpEOS = 8
    KindExpSet = 9
    KindExpChar = 10
    KindItemChar = 11
    KindCharRange = 12
    KindExpLoop = 13

@cython.cclass
class ExpBase:
    def __init__(self) -> None:
        self.kind = ExpKind.KindExpBase

@cython.cclass
class ExpRE(ExpBase):
    def __init__(self, exprs: List["ExpSimpleRE"]) -> None:
        self.kind = ExpKind.KindExpRE
        self.exprs = exprs

@cython.cclass
class ExpSimpleRE(ExpBase):
    def __init__(self, exprs: List["ExpBasicRE"]) -> None:
        self.kind = ExpKind.KindExpSimpleRE
        self.exprs = exprs

@cython.cclass
class ExpGroup(ExpBase):
    def __init__(self, group_type: str, expr: ExpRE) -> None:
        self.kind = ExpKind.KindExpGroup
        self._group_type = group_type
        self._expr = expr

@cython.cclass
class ExpAny(ExpBase):
    def __init__(self) -> None:
        self.kind = ExpKind.KindExpAny

@cython.cclass
class ExpEOS(ExpBase):
    def __init__(self) -> None:
        self.kind = ExpKind.KindExpEOS

@cython.cclass
class ExpSet(ExpBase):
    def __init__(self, positive: bool, items: List["ExpSetItem"]) -> None:
        self.kind = ExpKind.KindExpSet
        self._positive = positive
        self._items = items

@cython.cclass
class ExpChar(ExpBase):
    def __init__(self, c: cython.Py_UCS4) -> None:
        self.kind = ExpKind.KindExpChar
        self.c = c

@cython.cclass
class ItemChar(ExpBase):
    def __init__(self, c: cython.Py_UCS4) -> None:
        self.kind = ExpKind.KindItemChar
        self.c = c

@cython.cclass
class ItemCharRange(ExpBase):
    def __init__(self, start: cython.Py_UCS4, end: cython.Py_UCS4) -> None:
        self.kind = ExpKind.KindCharRange
        self._start = start
        self._end = end

ExpSetItem = Union[ItemChar, ItemCharRange]
ExpElementaryRE = Union[ExpGroup, ExpAny, ExpEOS, ExpSet, ExpChar]

@cython.cclass
class ExpLoop:
    def __init__(self, expr: ExpElementaryRE, start: cython.int, end: cython.int, lazy: cython.bint) -> None:
        self.kind = ExpKind.KindExpLoop
        self._expr = expr
        self._start = start
        self._end = end
        self._lazy = lazy

ExpBasicRE = Union[ExpElementaryRE, ExpLoop]
