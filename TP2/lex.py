import ply.lex as lex

import sys

states = [
    ('Funcao','exclusive'),
    ('Label','exclusive')
]

tokens = (
'ID',
'NUM',
'SETAD',
'SETAE',
'SWAP',
'IF',
'ELSE',
'WHILE',
'SWITCH',
'FUNC',
'RETURN'
)

t_ANY_ignore = ' \n\t'

literals = ['(',')','[',']','{','}',':',',']

t_ID = '[a-zA-Z]\w*' # \w contém o _ e não queremos vars a começar por _

t_NUM = '[0-9]+'

t_SETAD = '->'

t_SETAE = '<-'

t_SWAP = '<->'

t_IF = 'if'

t_ELSE = 'else'

t_WHILE = 'while'

t_SWITCH = 'switch'

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

lexer = lex.lex()


