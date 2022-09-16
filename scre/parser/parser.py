
from typing import List, Optional
import cython

from scre.parser.ast import ExpAny, ExpBase, ExpChar, ExpEOS, ExpGroup, ExpLoop, ExpRE, ExpSimpleRE, ExpBasicRE, ExpElementaryRE
from scre.basic.diagnostic import Diagnostic
from scre.basic.source import SourceLocation
from scre.basic.option_char import OptionChar

@cython.cclass
class CharIterator:
    def __init__(self, source: str, index: cython.int) -> None:
        self._source: str = source
        self._index: cython.int = index

    def next(self) -> OptionChar:
        if self._index < len(self._source):
            c = self._source[self._index]
            self._index += 1
            return OptionChar.Some(c)
        else:
            return OptionChar.Null()

    def advance_by(self, n: cython.int) -> cython.int:
        for i in range(n):
            if self.next().is_null():
                return i
        return n

    def nth(self, n: cython.int) -> OptionChar:
        self.advance_by(n)
        return self.next()
    
    def look_nth(self, n: cython.int) -> OptionChar:
        if self._index + n >= len(self._source):
            return OptionChar.Null()
        else:
            return OptionChar.Some(self._source[self._index + n])

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

    def nth_char(self, n: cython.int) -> OptionChar:
        return self.chars().nth(n)
    
    def first(self) -> OptionChar:
        return self._chars.look_nth(0)

    def second(self) -> OptionChar:
        return self._chars.look_nth(1)

    def is_eof(self) -> cython.bint:
        return self._chars._index >= len(self._chars._source)

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

    def bump(self) -> OptionChar:
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
            if fst.is_some() or fst.value() != '|':
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
        last_char_opt = self.first()
        if last_char_opt.is_some():
            last_char = last_char_opt.value()
            if last_char == "+":
                return ExpLoop(expr=expr, start=1, end=-1, lazy=False)
            elif last_char == "*":
                return ExpLoop(expr=expr, start=0, end=-1, lazy=False)
        
        return expr
    
    # @profile
    def parse_elementary(self) -> Optional[ExpElementaryRE]:
        char_opt = self.first()
        if char_opt.is_some():
            c = char_opt.value()
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

        if start.is_some() and start.value() == "(" and \
            end.is_some() and end.value() == ")":
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
        char_opt = self.bump()
        if char_opt.is_some():
            return ExpChar(char_opt.value())
        else:
            return None

    def parse_loop(self) -> Optional[ExpBase]:
        node = self.parse_group()
        loop_char_opt = self.first()
        if loop_char_opt.is_some():
            loop_char = loop_char_opt.value()
            if loop_char in ['+', '*']:
                self.bump()
                lazy_char = self.first()
                if lazy_char.is_some() and lazy_char.value() == '?':
                    return ExpLoop(node, loop_char, True)
                else:
                    return ExpLoop(node, loop_char, False)
        return node