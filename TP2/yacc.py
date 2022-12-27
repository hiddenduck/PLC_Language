import ply.yacc as yacc
import sys
from lex import tokens

#YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO provavelmente o lex deu asneira por causa das labels

type_table = {int}
id_table = dict()
id_local_table = dict()
label_table = dict()
scope = 0 #0->global; 1+->local
#++ x = (tipo, classe, localidade, endereço, dimenção)

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
    scope += 1

def p_if(p):
    "If : IfScope Exp Body"
    scope -= 1

def p_else_scope(p):
    "ElseScope : ELSE"
    #limpar scope anterior (if anterior)

def p_ielsef(p):
    "IfElse : IfScope Exp Body ElseScope Body"
    scope -= 1

def p_while_scope(p):
    "WhileScope : WHILE"
    scope += 1

def p_while(p):
    "While : WhileScope Exp Body"
    scope -= 1

def p_switch_scope(p):
    "SwitchScope : SWITCH"
    scope += 1


def p_switch(p):
    "Switch : SwitchScope Conds '{' Cases '}'"
    scope -= 1

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

def p_decl(p):
    "Decl: ID ID"
    if p[1] not in type_table:
        print("Semantic error. Type %s not included in typing set." % p[1])
        #invoke error?
    #Conseguir redeclarar dentro de um local scope e depois recuperar as declarações
    if p[2] in id_table:
        print("Semantic error. ID %s already included in global typing." % p[2])
        #invoke error?
    if p[2] in id_local_table:
       print("Semantic error. ID %s already included in local typing." % p[2])

    p[0] = r"pushi 0\n"
    id_local_table[p[2]] = {'classe' : 'var', 'endereco' : length(id_local_table), 'scope' : scope}


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
