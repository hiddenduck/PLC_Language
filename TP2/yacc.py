import ply.yacc as yacc
import sys
from lex import tokens

#YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO provavelmente o lex deu asneira por causa das labels


def p_axiom_code(p):
    "Axiom : Axiom Code"


def p_axiom_empty(p):
    "Axiom : "


def p_code_block(p):
    "Code : Code Block"


def p_code_empty(p):
    "Code : "


def p_block_exp(p):
    "Block : Exp ';'"


def p_block_if(p):
    "Block : If "


def p_block_ifelse(p):
    "Block : IfElse "


def p_block_while(p):
    "Block : While "


def p_block_switch(p):
    "Block : Switch "


def p_block_empty(p):
    "Block : "


def p_body_block(p):
    "Body : Block"


def p_body_code(p):
    "Body : '{' Code '}'"

def p_if_scope(p):
    "IfScope : IF"
    p.parser.scope_level += 1

def p_if(p):
    "If : IfScope Exp Body"
    p.parser.scope_level -= 1

def p_else_scope(p):
    "ElseScope : ELSE"
    #limpar scope anterior (if anterior)

def p_ielsef(p):
    "IfElse : IfScope Exp Body ElseScope Body"
    p.parser.scope_level -= 1

def p_while_scope(p):
    "WhileScope : WHILE"
    p.parser.scope_level += 1

def p_while(p):
    "While : WhileScope Exp Body"
    p.parser.scope_level -= 1

def p_switch_scope(p):
    "SwitchScope : SWITCH"
    p.parser.scope_level += 1


def p_switch(p):
    "Switch : SwitchScope Conds '{' Cases '}'"
    p.parser.scope_level -= 1

def p_conds_rec(p):
    "Conds : Conds ',' ID '(' Exp ')' "


def p_conds_base(p):
    "Conds : ID '(' Exp ')'"


def p_cases_rec(p):
    "Cases : Cases Case "


def p_cases_base(p):
    "Cases : Case"


def p_case(p):
    "Case: ID ':' Body"


def p_exp_atrib(p):
    "Exp: Atrib"


def p_exp_op(p):
    "Exp: Op"


def p_exp_decl(p):
    "Exp: Decl" 

def p_exp_declatrib(p):
    "Exp: DeclAtrib"

def p_declarray_name(p):
    "DeclArray : ID ArraySize"

def p_arraysize_num(p):
    "ArraySize : ArraySize '[' NUM ']'"

def p_arraysize_Atrib(p):
    "ArraySize : ArraySize '[' Atrib ']'"

def p_arraysize_Op(p):
    "ArraySize : ArraySize '[' Op ']'"

def p_arraysize_Id(p):
    "ArraySize : ArraySize '[' ID ']'"

def p_declatrib(p):
    "DeclAtrib : ID ID LARROW Exp"

def p_declatrib(p):
    "DeclAtrib : Exp RARROW ID ID"

def p_decl(p):
    "Decl: ID ID"
    t, v = 1,2
    if p[t] not in type_table:
        t,v = 2,1
        if p[t] not in type_table:
            print("Semantic error. Neither %s nor %s included in typing set." % (p[1],p[2]))
            #invoke error?
    #Conseguir redeclarar dentro de um local scope e depois recuperar as declarações
    if p[v] in id_table:
        print("Semantic error. ID %s already included in global typing." % p[v])
        #invoke error?
    if p[v] in id_local_table:
       print("Semantic error. ID %s already included in local typing." % p[v])

    p[0] = r"pushi 0\n"
    p.parser.id_table[p[v]] = {'classe' : 'var', 'endereco' : p.parser.n_local_vars, 'scope' : p.parser.scope, 'level' : p.parser.scope_level}
    p.parser.id_local_stack.append(p[v])
    p.parser.n_local_vars += 1


def p_atrib_left(p):
    "Atrib: ID LARROW Exp"


def p_atrib_right(p):
    "Atrib: Exp RARROW ID"


def p_atrib_equiv(p):
    "Atrib: ID SWAP ID"


def p_op_opuno(p):
    "Op: OpUno"


def p_op_opbin(p):
    "Op: OpBin"


def p_opuno_neg(p):
    "OpUno: NEG Exp"


def p_opuno_index(p):
    "OpUno: ID '[' Exp ']'"


def p_opbin_rec(p):
    "OpBin: OpBin OpLogic TermPlus"


def p_opbin_base(p):
    "OpBin: TermPlus"


def p_termplus_rec(p):
    "TermPlus: TermPlus OpPlus TermMult"


def p_termplus_base(p):
    "TermPlus: TermMult"


def p_termmult_rec(p):
    "TermMult: TermMult OpMult TermPow"


def p_termmult_base(p):
    "TermMult: TermPow"


def p_termpow_rec(p):
    "TermPow: TermPow OpPow Base"


def p_termmult_base(p):
    "TermPow: Base"
    

def p_base_exp(p):
    "Base: '(' Exp ')'"
    p[0] =   p[2]


def p_base_id(p):
    "Base: ID"
    p[0] = p[1]


def p_base_num(p):
    "Base: NUM"
    p[0] = p[1]


def p_oplogico_and(p):
    "OpLogico: AND"    
    p[0] = p[1]


def p_oplogico_or(p):
    "OpLogico: OR"    
    p[0] = p[1]


def p_oplogico_less(p):
    "OpLogico: LESS"    
    p[0] = p[1]


def p_oplogico_greater(p):
    "OpLogico: GREATER"    
    p[0] = p[1]


def p_oplogico_leq(p):
    "OpLogico: LEQ"   
    p[0] = p[1]


def p_oplogico_geq(p):
    "OpLogico: GEQ"  
    p[0] = p[1]


def p_oplogico_equal(p):
    "OpLogico: EQUAL"
    p[0] = p[1]


def p_opplus_add(p):
    "OpPlus: ADD"
    p[0] = p[1]


def p_opplus_sub(p):
    "OpPlus: SUB"
    p[0] = p[1]


def p_opmult_mul(p):
    "OpMult: MUL"
    p[0] = p[1]


def p_opmult_div(p):
    "OpMult: DIV"
    p[0] = p[1]


def p_oppow(p):
    "OpPow: POW"
    p[0] = p[1]

parser = yacc.yacc()

#0->global; 1+->local
#++ x = (tipo, classe, localidade, endereço, dimenção)
parser.type_table = {'int'}
parser.id_table = dict()
parser.id_local_stack = list()
parser.label_table = dict()
parser.scope_level = 0
parser.scope = 0
p.parser.n_local_vars = 0