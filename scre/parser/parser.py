from typing import List, Optional
import cython

from scre.parser.ast import ExpBase, ExpChar, ExpLoop, ExpOr, ExpSeq
from scre.basic.diagnostic import Diagnostic
from scre.basic.source import SourceLocation
from scre.basic.option_char import OptionChar

@cython.cclass
class CharIterator:
    def __init__(self, source: str, index: int) -> None:
        self._source: str = source
        self._index: int = index

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
        return self.nth_char(0)

    def second(self) -> OptionChar:
        return self.nth_char(1)

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

    def parse(self) -> Optional[ExpBase]:
        return self.parse_or()

    def parse_or(self) -> Optional[ExpBase]:
        exprs: List[ExpBase] = []
        node = self.parse_sequence()
        if node is None:
            self.error("Parse sequence error")
            return None

        while True:
            fst = self.bump()
            if fst.is_some() or fst.value() != '|':
                break
            node = self.parse_sequence()
            if node is None:
                break

        if len(exprs) == 1:
            return exprs[0]
        else:
            return ExpOr(exprs)

    def parse_sequence(self) -> Optional[ExpBase]:
        exprs: List[ExpBase] = []
        node = self.parse_unit()
        if node is None:
            self.error("Parse unit error")
            return None
        else:
            exprs.append(node)

        while True:
            node = self.parse_unit()
            if node is None:
                break
            else:
                exprs.append(node)

        if len(exprs) == 1:
            return exprs[0]
        else:
            return ExpSeq(exprs)

    def parse_unit(self) -> Optional[ExpBase]:
        return self.parse_loop()

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

    def parse_group(self) -> Optional[ExpBase]:
        first_char = self.first()
        if first_char.is_some():
            self.bump()
            return ExpChar(first_char.value())
        else:
            return None