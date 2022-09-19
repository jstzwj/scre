
from scre.core.pattern import Pattern
from scre.parser.parser import Parser
from scre.automata.builder import build_nfa

def compile(pattern: str, flags: int=0) -> Pattern:
    parser = Parser(pattern)
    ast = parser.parse()
    if len(parser.diagnostic) != 0:
        print(parser.diagnostic)
    dfa = build_nfa(ast)
    return Pattern(automaton=dfa)
