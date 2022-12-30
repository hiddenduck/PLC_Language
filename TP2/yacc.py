import ply.yacc as yacc
import sys
from lex import tokens

# YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO provavelmente o lex deu asneira por causa das labels
# Está pela ordem que aparecce na gramatica
# tem dois \n entre as funçoes para os pitoninhos nao gritarem comigo


def p_axiom_code(p):
    "Axiom : Axiom Code"
    p[0] = p[1] + p[2]


def p_axiom_function(p):
    "Axiom : Function"


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


def p_function(p):
    "Function : ID ':' FunCases '{' Body '}'"


def p_funcases_funextra_rarrow(p):
    "FunCases : FunExtra ID RARROW ID"


def p_funcases_rarrow(p):
    "FunCases : RARROW ID"


def p_funcases_funextra(p):
    "FunCases : FunExtra ID"


def p_funcases_empty(p):
    "FunCases : "


def p_funextra_rec(p):
    "FunExtra : ID ','"


def p_funextra_empty(p):
    "FunExtra : "


def p_if_scope(p):
    "IfScope : IF"
    p.parser.id_table_stack.append(dict())
    p.parser.scope_level += 1
    p[0] = p[1]


def p_if(p):
    "If : IfScope Exp Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1
    p[0] = p[2] + "jz end" + p.parser.internal_label + \
        "\n" + p[3] + "end" + p.parser.internal_label + ":\n"
    p.parser.internal_label += 1


def p_else_scope(p):
    "ElseScope : ELSE"
    p.parser.id_table_stack.pop()
    p.parser.id_table_stack.append(dict())
    # limpar scope anterior (if anterior)


def p_ifelse(p):
    "IfElse : IfScope Exp Body ElseScope Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1
    p[0] = p[2] + "jz else" + p.parser.internal_label + "\n" + \
        p[3] + "jump end" + (p.parser.internal_label + 1)
    + "\nelse" + p.parser.internal_label + ":\n" + \
        p[5] + "end" + (p.parser.internal_label + 1) + ":\n"
    p.parser.internal_label += 2


def p_while_scope(p):
    "WhileScope : WHILE"
    p.parser.id_table_stack.append(dict())
    p.parser.scope_level += 1


def p_while(p):
    "While : WhileScope Exp Body"
    p.parser.id_table_stack.pop()
    p.parser.scope_level -= 1
    l = p.parser.internal_label
    p[0] = "loop" + l + ":\n" + p[2] + "jz end" + \
        (l + 1) + "\n" + p[3] + "jump loop" + l + "\nend" + (l + 1) + ":\n"
    p.parser.internal_label += 2


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
    p[0] = p[1] + p[5]


def p_conds_base(p):
    "Conds : ID '(' Exp ')'"
    p[0] = p[3]


def p_cases_rec(p):
    "Cases : Cases Case "
    p[0] = p[1] + p[2]


def p_cases_base(p):
    "Cases : Case"
    p[0] = p[1]


def p_case(p):
    "Case: ID ':' Body"


def p_exp_atrib(p):
    "Exp: Atrib"
    p[0] = p[1]


def p_exp_op(p):
    "Exp; Op"


def p_exp_decl(p):
    "Exp: Decl"
    p[0] = p[1]


def p_exp_declarray(p):
    "Exp: DeclArray"


def p_exp_declatrib(p):
    "Exp: DeclAtrib"
    p[0] = p[1]


def p_atribop_atribnum(p):
    "AtribOp : AtribNum"


def p_atribop_op(p):
    "AtribOp : Op"


def p_decl(p):
    "Decl: ID ID"
    t, v = 1, 2
    if p[t] not in type_table:
        t, v = 2, 1
        if p[t] not in type_table:
            print("ERROR: Neither %s nor %s included in typing set." %
                  (p[1], p[2]))
            # invoke error?

        table = p.parser.id_table_stack[-1]
        if v in table:
            print("ERROR: %s already declared in local typing." % v)
            # invoke error
        # o endereço pode não ser o tamanho da tabela: arrays estragam a brincadeira
        table[v] = {'classe': 'var', 'endereco': len(table),
                    'scope': p.parser.scope, 'level': p.parser.scope_level, 'tipo': t}

        p[0] = r"pushi 0\n"


def p_declarray(p):
    "DeclArray : ID ID DeclArraySize"
    t, v = 1, 2
    if p[t] not in type_table:
        t, v = 2, 1
    if p[t] not in type_table:
        print("ERROR: Neither %s nor %s included in typing set." %
              (p[1], p[2]))
        # invoke error?
    table = p.parser.id_table_stack[-1]
    n_vars = p.parser.scope_n_vars.pop()

    if v in table:
        print("ERROR: %s already declared in local typing." % v)
        # invoke error
    table[v] = {'classe': 'array', 'n_dimensao': len(p[3]), 'tamanho': p[3], 'endereco': n_vars,
                'scope': p.parser.scope, 'level': p.parser.scope_level, 'tipo': t}

    p.parser.scope_n_vars.append(n_vars+1)


def p_declarraysize_rec(p):
    "DeclArraySize '[' NUM ']'"


def p_atribarray_Leftatribop(p):
    "AtribArray : ID ArraySize LARROW AtribOp"


def p_atribarray_Rightatribop(p):
    "AtribArray : AtribOp RARROW ID ArraySize"


def p_arraysize_rec(p):
    "ArraySize : ArraySize '[' AtribOp ']'"
    p[0] = p[1] + [p[2]]


def p_arraysize_empty(p):
    "ArraySize : "
    p[0] = []


def p_declatrib_left(p):
    "DeclAtrib : ID ID LARROW AtribOp"


def p_declatrib_right(p):
    "DeclAtrib : AtribOp RARROW ID ID"
    # 7+5 -> int  INT Int iNt x? #####vao permitir isto???#####
    if p[3] not in p.type_table:
        print("ERROR: invalid type")
    else:




def p_atribnum_left(p):
    "AtribNum : ID LARROW AtribOp"
    p[0] = p[3] + "dup 1\n" + gen_atrib_code_stack(p, p[1])


def p_atribnum_right(p):
    "AtribNum : AtribOp LARROW ID"
    # 2+4->x++
    p[0] = p[1] + "dup 1\n" + gen_atrib_code_stack(p, p[3])


def p_atribnum_array(p):
    "AtribNum : AtribArray"
    p[0] = p[1]


def p_atrib_left(p):
    "Atrib: ID LARROW AtribOp"
    p[0] = p[3] + gen_atrib_code_stack(p, p[1])


def p_atrib_right(p):
    "Atrib: AtribOp RARROW ID"
    p[0] = p[1] + gen_atrib_code_stack(p, p[3])


def p_atrib_equiv(p):
    "Atrib: ID SWAP ID"
    flag1 = flag2 = True
    for i in range(len(p.id_table_stack)-1, 0, -1):

        if p[1] in p.id_table_stack[i] and flag1:
            end1 = p.id_table_stack[i][p[1]]['endereco']
            flag1 = False
        if p[3] in p.id_table_stack[i] and flag2:
            end2 = p.id_table_stack[i][p[3]]['endereco']
            flag2 = False
        if not (flag1 or flag2):
            p[0] = f"pushl {end1}\npushl {end2}\nstorel {end1}\nstorel {end2}\n"
            return

    if p[1] not in p.id_table_stack[0] or p[3] not in p.id_table_stack[0]:
        # depois podemos por para dizer qual foi a gaja
        print("ERROR: one of the variables not in scope")
    else:
        p[0] = f"pushg {end1}\npushg {end2}\nstoreg {end1}\nstoreg {end2}\n"
    return


def p_atrib_array(p):
    "Atrib : AtribArray"
    p[0] = p[1]


def p_op_opuno(p):
    "Op: OpUno"
    p[0] = p[1]


def p_op_opbin(p):
    "Op: OpBin"
    p[0] = p[1]


def p_opuno_neg(p):
    "OpUno: NEG AtribOp"
    p[0] = p[2] + 'not\n'


def p_opuno_accessarray(p):
    "OpUno: AccessArray"
    p[0] = p[1]


def p_opuno_minus(p):
    "OpUno: SUB AtribOp"
    p[0] = "pushi 0\n" + p[2] + "sub\n"


def p_accessarray(p):
    "AccessArray: ID ArraySize"
    for i in range(len(p.id_table_stack)-1, 0, -1):
        if p[1] in p.id_table_stack[i]:
            end = p.id_table_stack[i][p[1]]['endereco']
            p[0] = f"pushl {end}\n" + p[2] + "loadn\n"
            return
    if p[1] not in p.id_table_stack[0]:
        print("ERROR: variable not in scope")
    else:
        end = p.id_table_stack[0][p[1]]['endereco']
        p[0] = f"pushg {end}\n" + p[2] + "loadn\n"
    return


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


def p_termpow_base(p):
    "TermPow: Base"
    p[0] = p[1]


def p_base_exp(p):
    "Base: '(' AtribOp ')'"
    p[0] = p[2]


def p_base_id(p):
    "Base: ID"
    for i in range(len(p.id_table_stack)-1, 0, -1):
        if p[1] in p.id_table_stack[i]:
            p[0] = "pushl %d\n" % p.id_table_stack[i][p[1]]['endereco']
            return
    if p[1] not in p.id_table_stack[0]:
        print("ERROR: variable not in scope")
    else:
        p[0] = "pushg %d\n" % p.id.id_table_stack[i][p[1]]['endereco']
    return


def p_base_num(p):
    "Base: NUM"
    p[0] = "pushi %d\n" % p[1]


def p_base_funcall(p):
    "Base : FunCall"
    p[0] = p[1]


def p_funcall(p):
    "FunCall : ID '(' FunArg ')'"
    s = ""
    s += p[3] + "pusha " + p.id_table_stack[0][p[1]]['label'] + "\n"
    s += "CALL\n"
    p[0] = s


def p_funarg_funrec(p):
    "FunArg : FunRec"
    p[0] = p[1]


def p_funarg_empty(p):
    "FunArg : "
    p[0] = ""


def p_funrec_rec(p):
    "FunRec : FunRec ',' AtribOp"
    p[0] = p[1] + p[3]


def p_funrec_base(p):
    "FunRec : AtribOp"
    p[0] = p[1]


def p_oplogico_and(p):
    "OpLogico: AND"
    p[0] = "and\n"


def p_oplogico_or(p):
    "OpLogico: OR"
    p[0] = "or\n"


def p_oplogico_lesser(p):
    "OpLogico: LESSER"
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


# eu pus este codigo aqui em baixo para nao misturar
# as cenas da gramatica com outro codigo


def gen_atrib_code(p, id, exp):
    s = ""
    if id not in p.parser.id_table:
        print("ERROR: Name %s not defined." % id)
        # invoke error
    elif p.parser.id_table[id]['scope'] == 0:
        # pensar que se deve colocar no topo da stack o valor no ID para se conseguir fazer a operação
        s = exp + "storeg %d\n" % p.parser.id_table[id]['endereco']
    elif p.parser.id_table[id]['scope'] == p.parser.scope:
        s = exp + "storel %d\n" % p.parser.id_table[id]['endereco']
    else:
        print("ERROR: Name %s defined elsewhere in program, not defined in local or global scope." % id)
        # invoke error
        return s


def gen_atrib_code_stack(p, id, atribop):
    s = ""
    for tamanho in range(len(p.id_table_stack)-1, 0, -1):
        if id in p.parser.id_table_stack[tamanho]:
            s = "storel %d\n" % p.parser.id_table_stack[tamanho][id]['endereco']
            break
    else:
        if id not in p.parser.id_table_stack[0]:
            print("ERROR: Name %s not defined." % id)
            # invoke error
        else:
            s = "storeg %d\n" % p.parser.id_table_stack[0][id]['endereco']
    return s


parser = yacc.yacc()

# 0->global; 1+->local
# ++ x = (tipo, classe, localidade, endereço, dimenção)
parser.type_table = {'int'}
parser.id_table_stack = list()
parser.scope_n_vars = list()
parser.label_table_stack = list()
parser.scope_level = 0
parser.scope = 0
parser.internal_label = 0
