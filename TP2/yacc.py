import ply.yacc as yacc
import sys
from lex import tokens

#YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO provavelmente o lex deu asneira por causa das labels


def p_axiom_code(p):
    "Axiom : Axiom Code"
    p[0] = p[1] + p[2]


def p_axiom_empty(p):
    "Axiom : "
    p[0] = ""

def p_code_block(p):
    "Code : Code Block"
    p[0] = p[1] + p[2]

def p_code_empty(p):
    "Code : "
    p[0] = ""

def p_block_exp(p):
    "Block : Exp ';'"
    p[0] = p[1]

def p_block_if(p):
    "Block : If "
    p[0] = p[1]

def p_block_ifelse(p):
    "Block : IfElse "
    p[0] = p[1]

def p_block_while(p):
    "Block : While "
    p[0] = p[1]

def p_block_switch(p):
    "Block : Switch "
    p[0] = p[1]

def p_block_empty(p):
    "Block : "
    p[0] = ""

def p_body_block(p):
    "Body : Block"
    p[0] = p[1]

def p_body_code(p):
    "Body : '{' Code '}'"
    p[0] = p[2]

def p_if_scope(p):
    "IfScope : IF"
    p.parser.id_table_stack.append(dict())
    p.parser.scope_level += 1

def p_if(p):
    "If : IfScope Exp Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1

def p_else_scope(p):
    "ElseScope : ELSE"
    p.parser.id_table_stack.pop()
    p.parser.id_table_stack.append(dict())
    #limpar scope anterior (if anterior)

def p_ielsef(p):
    "IfElse : IfScope Exp Body ElseScope Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1

def p_while_scope(p):
    "WhileScope : WHILE"
    p.parser.id_table_stack.append(dict())
    p.parser.scope_level += 1

def p_while(p):
    "While : WhileScope Exp Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1

def p_switch_scope(p):
    "SwitchScope : SWITCH"
    p.parser.id_table_stack.append(dict())
    p.parser.scope_level += 1


def p_switch(p):
    "Switch : SwitchScope Conds '{' Cases '}'"
    p.parser.id_table_stack.pop()
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
    p[0] = p[1]


def p_exp_op(p):
    "Exp: Op"
    p[0] = p[1]


def p_exp_decl(p):
    "Exp: Decl"
    p[0] = p[1]

def p_exp_declatrib(p):
    "Exp: DeclAtrib"
    p[0] = p[1]

def p_declarray_name(p):
    "DeclArray : ID ID ArraySize"

def p_arraysize_base(p):
    "ArraySize : "

def p_arraysize_rec(p):
    "ArraySize : ArraySize ArrayType"

def p_arraytype_num(p):
    "ArrayType : '[' NUM ']'"

def p_arraytype_Atrib(p):
    "ArrayType : '[' Atrib ']'"

def p_arraytype_Op(p):
    "ArrayType : '[' Op ']'"

def p_arraytype_Id(p):
    "ArrayType : '[' ID ']'"

def p_atribarray_LeftOP(p):
    "AtribArray : ID ArraySize LARROW Op"

def p_atribarray_LeftAtrib(p):
    "AtribArray : ID ArraySize LARROW Atrib"

def p_atribarray_RightOp(p):
    "AtribArray : Op RARROW ID ArraySize"

def p_atribarray_RightAtrib(p):
    "AtribArray : Atrib RARROW ID ArraySize"

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
            print("ERROR: Neither %s nor %s included in typing set." % (p[1],p[2]))
            #invoke error?
    #Conseguir redeclarar dentro de um local scope e depois recuperar as declarações
    #if p[v] in id_table:
    #    print("Semantic error. ID %s already included in global typing." % p[v])
        #invoke error?
    #if p[v] in id_local_table:
    #   print("Semantic error. ID %s already included in local typing." % p[v])

    table = p.parser.id_table_stack[-1]
    if v in table:
        print("ERROR: %s already declared in local typing." % v)
        #invoke error
    table[v] = {'classe' : 'var', 'endereco' : len(table), 'scope' : p.parser.scope, 'level' : p.parser.scope_level}

    p[0] = r"pushi 0\n"
    

def gen_atrib_code(p, id, exp):
    s = ""
    if id not in p.parser.id_table:
        print("ERROR: Name %s not defined." % id)
        #invoke error
    elif p.parser.id_table[id]['scope'] == 0:
        #pensar que se deve colocar no topo da stack o valor no ID para se conseguir fazer a operação
        s = exp + "storeg %d\n" % p.parser.id_table[id]['endereco']
    elif p.parser.id_table[id]['scope'] == p.parser.scope:
        s = exp + "storel %d\n" % p.parser.id_table[id]['endereco']
    else:
        print("ERROR: Name %s defined elsewhere in program, not defined in local or global scope." % id)
        #invoke error
    return s

def p_atrib_left(p):
    "Atrib: ID LARROW Exp"
    p[0] = gen_atrib_code(p, p[1], p[3])

def p_atrib_right(p):
    "Atrib: Exp RARROW ID"
    p[0] = gen_atrib_code(p, p[3], p[1])

def p_atrib_equiv(p):
    "Atrib: ID SWAP ID"
    if p[1] not in p.parser.id_table:
        print("ERROR: Name %s not defined." % p[1])
        #invoke error
    if p[3] not in p.parser.id_table:
        print("ERROR: Name %s not defined." % p[3])
        #invoke error
    s1 = p.parser.id_table[p[1]]['scope']
    if s1 == 0: s1 = "g"
    elif s1 == p.parser.scope: s1 = "l"
    else:
        print("ERROR: Name %s defined elsewhere in program, not defined in local or global scope." % p[1])
        #invoke error
    s3 = p.parser.id_table[p[3]]['scope']
    if s3 == 0: s3 = "g"
    elif s3 == p.parser.scope: s3 = "l"
    else:
        print("ERROR: Name %s defined elsewhere in program, not defined in local or global scope." % p[3])
        #invoke error
    s1 += " %d" % (p.parser.id_table[p[1]]['endereco'])
    s3 += " %d" % (p.parser.id_table[p[3]]['endereco'])
    p[0] = "push" + s3 + "\npush" + s1 + "\nstore" + s3 + "\nstore" + s1 + "\n"

def p_atrib_array(p):
    "Atrib : ID AtribArray"

def p_op_opuno(p):
    "Op: OpUno"
    p[0] = p[1]


def p_op_opbin(p):
    "Op: OpBin"
    p[0] = p[1]

def p_opuno_neg(p):
    "OpUno: NEG Exp"
    p[0] = p[2] + 'not\n'

def p_opuno_index(p):
    "OpUno: ID '[' Exp ']'"

def p_opuno_index(p):

def p_opbin_rec(p):
    "OpBin: OpBin OpLogic TermPlus"
    p[0] = p[1] + p[3] + p[2]

def p_opbin_base(p):
    "OpBin: TermPlus"
    p[0] = p[1]

def p_termplus_rec(p):
    "TermPlus: TermPlus OpPlus TermMult"
    p[0] = p[1] + p[3] + p[2]

def p_termplus_base(p):
    "TermPlus: TermMult"
    p[0] = p[1]

def p_termmult_rec(p):
    "TermMult: TermMult OpMult TermPow"
    p[0] = p[1] + p[3] + p[2]

def p_termmult_base(p):
    "TermMult: TermPow"
    p[0] = p[1]

def p_termpow_rec(p):
    "TermPow: TermPow OpPow Base"
    p[0] = p[1] + p[3] + p[2]

def p_termmult_base(p):
    "TermPow: Base"
    p[0] = p[1]

def p_base_exp(p):
    "Base: '(' Exp ')'"
    p[0] = p[2]


def p_base_id(p):
    "Base: ID"
    if p[1] not in p.parser.id_table:
        print("ERROR: Name %s not defined." % p[1])
        #invoke error
    elif p.parser.id_table[p[1]]['scope'] == 0:
        #pensar que se deve colocar no topo da stack o valor no ID para se conseguir fazer a operação
        p[0] = "pushg %d\n" % p.parser.id_table[p[1]]['endereco']
    elif p.parser.id_table[p[1]]['scope'] == p.parser.scope:
        p[0] = exp + "pushl %d\n" % p.parser.id_table[p[1]]['endereco']
    else:
        print("ERROR: Name %s defined elsewhere in program, not defined in local or global scope." % p[1])
        #invoke error

def p_base_num(p):
    "Base: NUM"
    p[0] = "pushi %d\n" % p[1]


def p_oplogico_and(p):
    "OpLogico: AND"    
    p[0] = "and\n"


def p_oplogico_or(p):
    "OpLogico: OR"    
    p[0] = "or\n"


def p_oplogico_less(p):
    "OpLogico: LESS"    
    p[0] = "inf\n"


def p_oplogico_greater(p):
    "OpLogico: GREATER"    
    p[0] = "sup\n"


def p_oplogico_leq(p):
    "OpLogico: LEQ"   
    p[0] = "infeq\n"


def p_oplogico_geq(p):
    "OpLogico: GEQ"  
    p[0] = "supeq\n"


def p_oplogico_equal(p):
    "OpLogico: EQUAL"
    p[0] = "equal\n"


def p_opplus_add(p):
    "OpPlus: ADD"
    p[0] = "add\n"


def p_opplus_sub(p):
    "OpPlus: SUB"
    p[0] = "sub\n"


def p_opmult_mul(p):
    "OpMult: MUL"
    p[0] = "mul\n"


def p_opmult_div(p):
    "OpMult: DIV"
    p[0] = "div\n"


def p_oppow(p):
    "OpPow: POW"
    p[0] = p[1]

parser = yacc.yacc()

#0->global; 1+->local
#++ x = (tipo, classe, localidade, endereço, dimenção)
parser.type_table = {'int'}
parser.id_table_stack = list()
parser.lable_table_stack = list()
parser.scope_level = 0
parser.scope = 0