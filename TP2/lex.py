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
'SWITCHCOND',
'SWITCHCASE',
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
'POW',
'READ',
'PRINT'
)

t_ANY_ignore = ' \n\t'

literals = ['(',')','[',']','{','}',':',',',';']

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'switchcond' : 'SWITCHCOND',
    'switchcase' : 'SWITCHCASE'
}

t_RARROW = r'-+>'

t_LARROW = r'<-+'

t_SWAP = r'<-+>'

t_NEG = r'~ | !'

t_AND = r'&'

t_OR = r'\|'

t_LESSER = r'<'

t_GREATER = r'>'

t_LEQ = r'<='

t_GEQ = r'>='

t_EQUAL = r'=+'

t_ADD = r'\+'

#O lex não consegue apanhar o a -1 porque acha que (-1) é um número oops
t_SUB = r'-'

t_MUL = r'\*'

t_DIV = r'/'

t_POW = r'\^'

t_PRINT = r'\>\?'

t_READ = r'\<\?'

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

def t_ID(t):
    r'[a-zA-Z]\w*' # \w contém o _ e não queremos vars a começar por _
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
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

#for linha in sys.stdin:
#    lexer.input(linha)
#    tok = lexer.token()
#    while tok:
#        print(tok)
#        tok = lexer.token()
