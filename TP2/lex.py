import ply.lex as lex

import sys

states = [
    ('Funcao','exclusive'),
    ('Label','exclusive')
]

tokens = (
'ID',
'NUM',
'RARROW',
'LARROW',
'SWAP',
'IF',
'ELSE',
'WHILE',
'SWITCH',
'FUNC',
'RETURN',
'NEG',
'AND',
'OR',
'LESSER',
'GREATER',
'LEQ',
'GEQ',
'EQUAL',
'ADD',
'SUB',
'MUL',
'DIV',
'POW'
)

t_ANY_ignore = ' \n\t'

literals = ['(',')','[',']','{','}',':',',',';']

t_ID = '[a-zA-Z]\w*' # \w contém o _ e não queremos vars a começar por _

def t_NUM(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

t_RARROW = '-+>'

t_LARROW = '<-+'

t_SWAP = '<-+>'

t_IF = 'if'

t_ELSE = 'else'

t_WHILE = 'while'

t_SWITCH = 'switch'

t_NEG = '~ | !'

t_AND = '&'

t_OR = '\|'

t_LESSER = '<'

t_GREATER = '>'

t_LEQ = '<='

t_GEQ = '>='

t_EQUAL = '=+'

t_ADD = '\+'

t_SUB = '-'

t_MUL = '\*'

t_DIV = '/'

t_POW = '\^'


def t_ANY_error(t):
    print('Illegal character: %s', t.value[0])


def t_FUNC(t):
    r'def'
    t.lexer.begin('Funcao')
    return t

def t_Funcao_RETURN(t):
    r'rekt'
    t.lexer.begin('INITIAL')
    return t

#Isto vai dar barraco 100% -> tentar fazer vários estados para ter LABELS e IDS
def t_Label_LABEL(t):
    r'[a-zA-Z]\w*'
    t.lexer.begin('Cond')
    return t

"""def t_Label_out(t):
    r'('
    t.lexer.begin('Cond')
    return t

#def t_Cond(t):
    r','
    t.lexer.begin('Label')
    return t

def t_Cond(t):
    r'{'
    t.lexer.begin('INITIAL')
    return t"""

lexer = lex.lex()

for linha in sys.stdin:
    lexer.input(linha)
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()
