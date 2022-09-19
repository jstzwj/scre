import cython
from scre.automata.graph import Automaton
from scre.parser.ast import ExpAny, ExpChar, ExpEOS, ExpElementaryRE, ExpGroup, ExpKind, ExpLoop, ExpRE, ExpSet, ExpSimpleRE, ExpBasicRE

@cython.boundscheck(False)
@cython.nonecheck(False)
def join_automaton(lhs, rhs):
    ret = Automaton()
    ret._states.append(lhs.start)
    ret._states.append(rhs.end)
    ret._start = 0
    ret._end = 1

    i: cython.int = 0
    lhs_len: cython.int = len(lhs._states)
    while i < lhs_len:
        if i != lhs._start and i != lhs._end:
            ret._states.append(lhs._states[i])
        i += 1
    i: cython.int = 0
    rhs_len: cython.int = len(rhs._states)
    while i < rhs_len:
        if i != rhs._start and i != rhs._end:
            ret._states.append(rhs._states[i])
        i += 1

    for lhs_end in lhs.end.ins:
        lhs_end.outs.remove(lhs.end)
        
        for rhs_start in rhs.start.outs:
            lhs_end.outs.append(rhs_start)
            rhs_start.ins.remove(rhs.start)
            rhs_start.ins.append(lhs_end)

    return ret

@cython.boundscheck(False)
@cython.nonecheck(False)
def union_automaton(lhs, rhs):
    ret = Automaton()
    ret._states.append(lhs.start)
    ret._states.append(lhs.end)
    ret._start = 0
    ret._end = 1

    i: cython.int = 0
    lhs_len: cython.int = len(lhs._states)
    while i < lhs_len:
        if i != lhs._start and i != lhs._end:
            ret._states.append(lhs._states[i])
        i += 1
    i: cython.int = 0
    rhs_len: cython.int = len(rhs._states)
    while i < rhs_len:
        if i != rhs._start and i != rhs._end:
            ret._states.append(rhs._states[i])
        i += 1

    for rhs_start in rhs.start.outs:
        rhs_start.ins.remove(rhs.start)
        rhs_start.ins.append(lhs.start)
        ret.start.outs.append(rhs_start)
    
    for rhs_end in rhs.end.ins:
        rhs_end.outs.remove(rhs.end)
        rhs_end.outs.append(lhs.end)
        ret.end.ins.append(rhs_end)

    return ret

def build_char(ast):
    assert ast.kind == 10
    automaton = Automaton()
    start = automaton.add_virtual_element()
    end = automaton.add_virtual_element()
    automaton.set_start(0)
    automaton.set_end(1)

    state = automaton.add_element(ast.c)

    automaton.connect(automaton.start, state)
    automaton.connect(state, automaton.end)

    return automaton

def build_elementary(ast):
    if ast.kind == 10:
        return build_char(ast)
    elif ast.kind == 6:
        return build_elementary(ast)
    elif ast.kind == 7:
        return build_loop(ast)
    elif ast.kind == 8:
        return build_loop(ast)
    elif ast.kind == 9:
        return build_loop(ast)
    
def build_loop(ast):
    assert ast.kind == 13

def build_basic(ast):
    # ExpElementaryRE or ExpLoop
    if ast.kind == 13:
        return build_loop(ast)
    else:
        return build_elementary(ast)

def build_simplere(ast):
    if ast.kind == 2:
        automaton = None
        for expr in ast.exprs:
            sub_automaton = build_basic(expr)
            if automaton is not None:
                automaton = join_automaton(automaton, sub_automaton)
            else:
                automaton = sub_automaton
        return automaton
    else:
        return build_basic(ast)

def build_nfa(ast):
    if ast.kind == 1:
        automaton = None
        for expr in ast.exprs:
            sub_automaton = build_simplere(expr)
            if automaton is not None:
                automaton = union_automaton(automaton, sub_automaton)
            else:
                automaton = sub_automaton
        return automaton
    else:
        return build_simplere(ast)