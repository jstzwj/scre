
from typing import List, Optional
import cython
import numpy as np

from scre.parser.ast import ExpAny, ExpBase, ExpChar, ExpEOS, ExpGroup, ExpLoop, ExpRE, ExpSimpleRE, ExpBasicRE, ExpElementaryRE
from scre.basic.diagnostic import Diagnostic
from scre.basic.source import SourceLocation

@cython.cclass
class CharIterator:
    def __init__(self, source: str, index: cython.int) -> None:
        self._source: str = source
        self._len: cython.int = len(source)
        self._index: cython.int = index

    @cython.boundscheck(False)
    def next(self) -> cython.Py_UCS4:
        c = cython.declare(cython.Py_UCS4)
        if self._index < self._len:
            c = self._source[self._index]
            self._index += 1
            return c
        else:
            return '\0'

    def advance_by(self, n: cython.int) -> cython.int:
        for i in range(n):
            if self.next() == '\0':
                return i
        return n

    def nth(self, n: cython.int) -> cython.Py_UCS4:
        self.advance_by(n)
        return self.next()
    
    @cython.boundscheck(False)
    def look_nth(self, n: cython.int) -> cython.Py_UCS4:
        if self._index + n >= self._len:
            return '\0'
        else:
            return self._source[self._index + n]

    @cython.boundscheck(False)
    def as_str(self) -> str:
        return self._source[self._index:]

@cython.cclass
class Parser:
    def __init__(self, source: str) -> None:
        self._source = source
        self._chars = CharIterator(source, 0)
        self._diagnostic: Diagnostic = Diagnostic()
        self._cursor_stack: List[int] = []

    @property
    def diagnostic(self) -> Diagnostic:
        return self._diagnostic

    def chars(self) -> CharIterator:
        return CharIterator(self._chars._source, self._chars._index)

    def nth_char(self, n: cython.int) -> cython.Py_UCS4:
        return self.chars().nth(n)
    
    def first(self) -> cython.Py_UCS4:
        return self._chars.look_nth(0)

    def second(self) -> cython.Py_UCS4:
        return self._chars.look_nth(1)

    def is_eof(self) -> cython.bint:
        return self._chars._index >= self._chars._len

    def push_cursor(self) -> None:
        index = self._chars._index
        self._cursor_stack.append(index)

    def pop_cursor(self) -> None:
        index = self._cursor_stack.pop()
        self._chars._index = index
    
    def drop_cursor(self) -> None:
        self._cursor_stack.pop()

    def error(self, msg: str) -> None:
        self._diagnostic.error(msg, SourceLocation(self._chars._source, self._chars._index))

    def bump(self) -> cython.Py_UCS4:
        return self._chars.next()

    # @profile
    def parse(self) -> Optional[ExpBase]:
        return self.parse_union()

    # @profile
    def parse_union(self) -> Optional[ExpSimpleRE]:
        exprs: List[ExpSimpleRE] = []
        node = self.parse_concatenation()
        if node is None:
            self.error("Parse concatenation error")
            return None
        else:
            exprs.append(node)

        while True:
            fst = self.bump()
            if fst == '\0' or fst != '|':
                break
            node = self.parse_concatenation()
            if node is None:
                break
            exprs.append(node)

        if len(exprs) == 1:
            return exprs[0]
        else:
            return ExpRE(exprs)

    # @profile
    def parse_concatenation(self) -> Optional[ExpBasicRE]:
        exprs: List[ExpBasicRE] = []
        node = self.parse_basic()
        if node is None:
            self.error("Parse unit error")
            return None
        else:
            exprs.append(node)

        while True:
            node = self.parse_basic()
            if node is None:
                break
            else:
                exprs.append(node)

        if len(exprs) == 1:
            return exprs[0]
        else:
            return ExpSimpleRE(exprs)

    # @profile
    def parse_basic(self) -> Optional[ExpBasicRE]:
        expr = self.parse_elementary()
        last_char = self.first()
        if last_char != '\0':
            if last_char == "+":
                return ExpLoop(expr=expr, start=1, end=-1, lazy=False)
            elif last_char == "*":
                return ExpLoop(expr=expr, start=0, end=-1, lazy=False)
        
        return expr
    
    # @profile
    def parse_elementary(self) -> Optional[ExpElementaryRE]:
        c = self.first()
        if c != '\0':
            if c == "(":
                return self.parse_group()
            elif c == ".":
                return self.parse_any()
            elif c == "$":
                return self.parse_eos()
            else:
                return self.parse_char()
        return None
    
    def parse_group(self) -> Optional[ExpGroup]:
        start = self.bump()
        expr = self.parse_any()
        end = self.bump()

        if start != '\0' and start == "(" and \
            end != '\0' and end == ")":
            return ExpGroup("Matched", expr)
        else:
            return None
    
    def parse_any(self) -> Optional[ExpAny]:
        self.bump()
        return ExpAny()

    def parse_eos(self) -> Optional[ExpEOS]:
        self.bump()
        return ExpEOS()

    # @profile
    def parse_char(self) -> Optional[ExpChar]:
        c = self.bump()
        if c != '\0':
            return c
        else:
            return None

    def parse_loop(self) -> Optional[ExpBase]:
        node = self.parse_group()
        loop_char_opt = self.first()
        if loop_char_opt != '\0':
            loop_char = loop_char_opt
            if loop_char in ['+', '*']:
                self.bump()
                lazy_char = self.first()
                if lazy_char != '\0' and lazy_char == '?':
                    return ExpLoop(node, loop_char, True)
                else:
                    return ExpLoop(node, loop_char, False)
        return node