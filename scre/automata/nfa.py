
from enum import auto
from scre.automata.graph import Automaton, join_automaton, union_automaton
from scre.parser.ast import ExpAny, ExpChar, ExpEOS, ExpElementaryRE, ExpGroup, ExpLoop, ExpRE, ExpSet, ExpSimpleRE, ExpBasicRE

def build_char(ast: ExpChar):
    automaton = Automaton()
    state = automaton.add_element(ast._char)
    automaton.start.outs.clear()
    automaton.end.ins.clear()
    automaton.connect(automaton.start, state)
    automaton.connect(state, automaton.end)
    return automaton

def build_elementary(ast: ExpElementaryRE):
    if isinstance(ast, ExpGroup):
        return build_elementary(ast)
    elif isinstance(ast, ExpAny):
        return build_loop(ast)
    elif isinstance(ast, ExpEOS):
        return build_loop(ast)
    elif isinstance(ast, ExpSet):
        return build_loop(ast)
    elif isinstance(ast, ExpChar):
        return build_char(ast)

def build_loop(ast: ExpLoop):
    pass

def build_basic(ast: ExpBasicRE):
    # ExpElementaryRE or ExpLoop
    if isinstance(ast, ExpElementaryRE):
        return build_elementary(ast)
    elif isinstance(ast, ExpLoop):
        return build_loop(ast)

def build_simplere(ast: ExpSimpleRE):
    if hasattr(ast, "_exprs"):
        automaton = Automaton()
        for expr in ast._exprs:
            sub_automaton = build_basic(expr)
            automaton = join_automaton(automaton, sub_automaton)
        return automaton
    else:
        return build_basic(ast)

def build_nfa(ast: ExpRE):
    if hasattr(ast, "_exprs"):
        automaton = Automaton()
        for expr in ast._exprs:
            sub_automaton = build_simplere(expr)
            automaton = union_automaton(automaton, sub_automaton)
        return automaton
    else:
        return build_simplere(ast)