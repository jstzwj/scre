from scre.automata.graph cimport Automaton, State
from scre.parser.ast cimport ExpBase, ExpChar, ExpGroup, ExpLoop, ExpRE, ExpSimpleRE

cdef join_automaton(Automaton lhs, Automaton rhs)
cdef union_automaton(Automaton lhs, Automaton rhs)

cpdef build_nfa(ExpBase ast)
cdef build_simplere(ExpBase ast)
cdef build_char(ExpChar ast)
cdef build_elementary(ExpBase ast)
cdef build_loop(ExpBase ast)
cdef build_basic(ExpBase ast)