"""
BNF
    BROADCAST   ::= '{' FORMULA '}' FORMULA
                 |  FORMULA
    FORMULA     ::= SYMBOL
                 |  FORMULA '->' FORMULA      # right associative
                 |  FORMULA '|' FORMULA       # left associative
                 |  FORMULA '&' FORMULA       # left associative
                 |  '~' FORMULA 
                 |  '[]' FORMULA
                 |  '<>' FORMULA
                 |  MODAL FORMULA
                 |  '(' FORMULA ')'
    MODAL       ::= '[' SYMBOL ']'
                 |  '<' SYMBOL '>'
    SYMBOL      ::= [a-zA-Z]\w*
"""

tokens = (
    'SYMBOL', 'IMPLIES', 'OR', 'AND',
    'NOT', 'NECESSARY', 'POSSIBLE',
    'LPARENTESIS', 'RPARENTESIS',
    'LNECESSARY', 'RNECESSARY',
    'LPOSSIBLE', 'RPOSSIBLE',
    'LBROADCAST', 'RBROADCAST'
    )

t_SYMBOL = r'[a-zA-Z_]*\w'
t_IMPLIES = r'->'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_NECESSARY = r'\[\]'
t_POSSIBLE = r'\<\>'
t_LPARENTESIS = r'\('
t_RPARENTESIS = r'\)'
t_LNECESSARY = r'\['
t_RNECESSARY = r'\]'
t_LPOSSIBLE = r'\<'
t_RPOSSIBLE = r'\>'
t_LBROADCAST = r'\{'
t_RBROADCAST = r'\}'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (("right", "IMPLIES"),
              ("left", "OR"),
              ("left", "AND"),
              ("right", "NOT"),
              ("right", "POSSIBLE"),
              ("right", "NECESSARY"),
              ("left", "LPOSSIBLE"),
              ("right", "RPOSSIBLE"),
              ("left", "LNECESSARY"),
              ("right", "RNECESSARY"))

def p_broadcast(p):
    '''BROADCAST : FORMULA
                  | LBROADCAST FORMULA RBROADCAST FORMULA'''
    p[0] = [p[2], '{}', p[4]] if len(p) == 5 else p[1]

def p_formula_proposition(p):
    'FORMULA : SYMBOL'
    p[0] = p[1]

def p_formula_binary(p):
    '''FORMULA : FORMULA IMPLIES FORMULA
                | FORMULA OR FORMULA
                | FORMULA AND FORMULA'''
    p[0] = [p[1], p[2], p[3]]

def p_formula_unary(p):
    '''FORMULA : NOT FORMULA
                | NECESSARY FORMULA
                | POSSIBLE FORMULA
                | MODAL FORMULA'''
    p[0] = [p[1], p[2]]

def p_formula_group(p):
    'FORMULA : LPARENTESIS FORMULA RPARENTESIS'
    p[0] = p[2]

def p_modal_necessity(p):
    '''MODAL : LNECESSARY SYMBOL RNECESSARY'''
    p[0] = [p[2], '[]']

def p_modal_possible(p):
    '''MODAL : LPOSSIBLE SYMBOL RPOSSIBLE'''
    p[0] = [p[2], '<>']

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse(s):
    return parser.parse(s)