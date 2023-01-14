import ply.yacc as yacc
import sys
from lex import tokens
from math import prod

def p_axiom_start(p):
    "Axiom : Start"
    main = "pusha main\ncall\n" if p.parser.main else ""
    p.parser.final_code = "start\n" + \
        p[1] + main + pop_local_vars(p) + "stop\n" + \
        "".join(p.parser.function_buffer)


def p_start_empty(p):
    "Axiom : "
    p.parser.final_code = ""


def p_axiom_code(p):
    "Start : Start Block"
    #p[0] = "\n".join(p.parser.function_buffer) + "start" + p[1] + p[2] + "stop"
    p[0] = p[1] + p[2]


def p_axiom_function(p):
    "Start : Start Function"
    # p.parser.function_buffer
    p[0] = p[1]


def p_axiom_empty(p):
    "Start : "
    p[0] = ""


def p_code_block(p):
    "Code : Code Block"
    p[0] = p[1] + p[2]


def p_code_empty(p):
    "Code : Block"
    p[0] = p[1]


def p_block_funcall(p):
    "Block : FunCall ';'"
    if p[1][1]:
        p[0] = p[1][0] + "pop 1\n"
    else:
        p[0] = p[1][0]


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


# def p_block_empty(p):
#    "Block : "
#    p[0] = ""

def p_body_empty(p):
    "Body : '{' '}'"
    p[0] = ""


def p_body_block(p):
    "Body : Block"
    p[0] = p[1]


def p_body_code(p):
    "Body : '{' Code '}'"
    p[0] = p[2]


def p_function(p):
    "Function : ID FunScope FunCases Body"
    label = p.parser.internal_label
    num_args = len(p[3][1])
    p.parser.function_table[p[1]] = {'num_args': num_args,
                                     'return': p[3][0],
                                     'label': f"F{label}"}

    s = ""

    local_args = len(p.parser.id_table_stack[-1])-int(num_args)
    if local_args > 0:
        #deixar se houver retorno e não houver argumentos
        s += "pop %d\n" % (local_args - int(num_args == 0 and p[3][0]))
    p.parser.local_adress = 0
    p.parser.id_table_stack.pop()
    #Se a função devolve ou não algo. p[3] é um tuplo.

    s_label = f"F{label}:\n"

    if p[1] == 'main':
        p.parser.main = True
        s_label = f"main:\n"

    if p[3][0]:
        p.parser.function_buffer.append(
            s_label + "pushi 0\n" + p[4] + \
            f"pushl 0\nstorel {-num_args}\n" + s + "return\n")
    else:
        p.parser.function_buffer.append(
            s_label + p[4] + s + "return\n")


    p[0] = ""
    p.parser.internal_label += 1
    p.parser.local_adress = p.parser.global_adress


def p_funscope(p):
    "FunScope : ':'"
    p.parser.id_table_stack.append(dict())
    p[0] = p[1]


def p_funcases_funextra_rarrow(p):
    "FunCases : FunExtra RARROW ID"
    p.parser.id_table_stack[-1][p[3]] = {'classe': 'var',
                                         'endereco': 0,
                                         'tamanho': [1],
                                         'tipo': 'int'}

    for i in range(1, len(p[1])+1):
        if p[1][-i] not in p.parser.id_table_stack[-1]:
            p.parser.id_table_stack[-1][p[1][-i]] = {'classe': 'var',
                                                     'endereco': -i,
                                                     'tamanho': [1],
                                                     'tipo': 'int'}
        else:
            print("ERROR: Variable %s already declared locally." % p[1][-i],file=sys.stderr)
            p_error(p)
    p[0] = (True, p[1])
    p.parser.local_adress = 1


def p_funcases_rarrow(p):
    "FunCases : RARROW ID"
    p.parser.id_table_stack[-1][p[2]] = {'classe': 'var',
                                         'endereco': 0,
                                         'tamanho': [1],
                                         'tipo': 'int'}
    p[0] = (True, [])
    p.parser.local_adress = 1


def p_funcases_funextra(p):
    "FunCases : FunExtra"
    for i in range(1, len(p[1])+1):
        if p[1][-i] not in p.parser.id_table_stack[-1]:
            p.parser.id_table_stack[-1][p[1][-i]] = {'classe': 'var',
                                                     'endereco': -i,
                                                     'tamanho': [1],
                                                     'tipo': 'int'}
        else:
            print("ERROR: Variable %s already declared locally." % p[1][-i],file=sys.stderr)
            p_error(p)
    p[0] = (False, p[1])


def p_funcases_empty(p):
    "FunCases : "
    p[0] = (False, [])


def p_funextra_rec(p):
    "FunExtra : FunExtra ',' ID"
    p[0] = p[1]
    p[0].append(p[3])


def p_funextra_empty(p):
    "FunExtra : ID"
    p[0] = [p[1]]


def p_if_scope(p):
    "IfScope : IF"
    p.parser.id_table_stack.append(dict())
    p[0] = p[1]


def p_if(p):
    "If : IfScope AtribOp Body"
    label = p.parser.internal_label
    p[0] = p[2] + \
        f"jz I{label}\n" + \
        p[3] + \
        f"I{label}:\n"
    p.parser.internal_label += 1

    p[0] += pop_local_vars(p)


def p_else_scope(p):
    "ElseScope : ELSE"
    pop_local_vars(p)  # pop do if
    p.parser.id_table_stack.append(dict())
    # limpar scope anterior (if anterior)
    p[0] = p[1]


def p_ifelse(p):
    "IfElse : IfScope AtribOp Body ElseScope Body"

    label = p.parser.internal_label
    p[0] = p[2] + f"jz I{label}\n" + \
        p[3] + \
        f"jump E{label}\n" + \
        f"I{label}:\n" + \
        p[5] + \
        f"E{label}:\n"
    p.parser.internal_label += 1

    p[0] += pop_local_vars(p)  # pop do else


def p_while_scope(p):
    "WhileScope : WHILE"
    p.parser.id_table_stack.append(dict())
    p[0] = p[1]


def p_while(p):
    "While : WhileScope '(' AtribOp ')' Body"

    lable_num = p.parser.internal_label

    pop_local = pop_local_vars(p)

    p[0] = f"W{lable_num}:\n" + \
        p[3] + \
        f"jz WE{lable_num}\n" + \
        p[5] + \
        pop_local + \
        f"jump W{lable_num}\n" + \
        f"WE{lable_num}:\n" + \
        pop_local

    p.parser.internal_label += 1


def p_switch_scopecond(p):
    "SwitchScope : SWITCHCOND"
    p.parser.id_table_stack.append(dict())
    p.parser.label_table_stack.append(
        (  # -----isto ´e um tuplo
            {':': list()},
            {':': list()}
        )  # -----
    )  # cond,cases
    # inicializar com o caracter especial e uma lista vazia
    p[0] = 2

def p_switch_scopecase(p):
    "SwitchScope : SWITCHCASE"
    p.parser.id_table_stack.append(dict())
    p.parser.label_table_stack.append(
        (  # -----isto ´e um tuplo
            {':': list()},
            {':': list()}
        )  # -----
    )  # cond,cases
    # inicializar com o caracter especial e uma lista vazia
    p[0] = 4


def p_switch(p):
    # aqui eu ja tenho as duas tabelas
    # acho que nao vai ser preciso o Conds
    "Switch : SwitchScope Conds '{' Cases '}'"

    cond_table = p.parser.label_table_stack[-1][0]
    case_table = p.parser.label_table_stack[-1][1]

    # testes de integridade das tabelas
    if cond_table.keys() != case_table.keys():
        print("ERROR: Condition labels don't match case labels",file=sys.stderr)
        p_error(p)
    if len(cond_table[':']) != len(case_table[':']):
        # estou a fazer com que todas as condiçoes apareçam e sejam chamadas uma vez (pode ser mudado)
        print("ERROR: Number of unlabeled conditions doesn't match number of unlabeled cases",file=sys.stderr)
        p_error(p)

    end_label_num = p.parser.internal_label
    p.parser.internal_label += 1

    p[0] = ""

    for label in p[p[1]]:  # percorrer ap[0]chamadas
        lab_num = p.parser.internal_label
        if label == ':':
            cond = cond_table[':'].pop(0)
            case = case_table[':'].pop(0)

        else:
            cond = cond_table[label]
            case = case_table[label]

        p[0] += cond + f"jz S{lab_num}\n" + case + \
            f"jump SE{end_label_num}\n" + f"S{lab_num}:\n"
        p.parser.internal_label += 1

    p[0] += f"SE{end_label_num}:\n"
    p[0] += pop_local_vars(p)
    p.parser.label_table_stack.pop()  # tirar as duas tabelas da stack


# nas conds passar para cima um par (conds_com_lable (dict?), conds_sem_lable (lista?))
def p_conds_rec(p):
    "Conds : Conds ',' Cond"
    p[0] = p[1]
    p[0].append(p[3])


def p_conds_base(p):
    "Conds : Cond"
    p[0] = list(p[1])


def p_cond_id(p):
    "Cond : ID '(' AtribOp ')'"
    p.parser.label_table_stack[-1][0][p[1]] = p[3]
    p[0] = p[1]


def p_cond_empty(p):
    "Cond : '(' AtribOp ')'"
    p.parser.label_table_stack[-1][0][':'].append(p[2])
    p[0] = ':'


def p_cases_rec(p):
    "Cases : Cases Case "
    p[0] = p[1]
    p[0].append(p[2])


def p_cases_base(p):
    "Cases : Case"
    p[0] = list(p[1])


def p_case_id(p):
    "Case : ID ':' Body"
    # preciso ver se ja tem la para dar erro
    p.parser.label_table_stack[-1][1][p[1]] = p[3]
    p[0] = p[1]  # ~acho que podemos ignorar isto mas whatever


def p_case_empty(p):
    "Case : ':' Body"
    # o par no label stack seria cond,case
    p.parser.label_table_stack[-1][1][':'].append(p[2])
    p[0] = ':'


"""def p_exp_funcall(p):
    "Exp : FunCall"
    if p[1][1]:
        p[0] = p[1][0] + "pop 1\n"
    else:
        p[0] = p[1][0]"""

def p_exp_print(p):
    "Exp : STRING PRINT"
    # funciona para tudo que não seja array
    p[0] = "pushs " + p[1] + "\nwrites\n" + r'pushs "\n"' + "\nwrites\n"

def p_exp_atrib(p):
    "Exp : Atrib"
    p[0] = p[1]


def p_exp_op(p):
    "Exp : Op"
    p[0] = p[1] + "pop 1\n"


def p_exp_decl(p):
    "Exp : Decl"
    p[0] = p[1]


def p_exp_declarray(p):
    "Exp : DeclArray"
    p[0] = p[1]


def p_exp_declatrib(p):
    "Exp : DeclAtrib"
    p[0] = p[1]


def p_atribop_atribnum(p):
    "AtribOp : AtribNum"
    p[0] = p[1]


def p_atribop_op(p):
    "AtribOp : Op"
    p[0] = p[1]


def p_decl(p):
    "Decl : ID ID"
    if p[1].lower() not in p.parser.type_table:
        print("ERROR : invalid type",file=sys.stderr)
    else:
        p[0] = "pushi 0\n"
        if len(p.parser.id_table_stack) == 1:
            p.parser.id_table_stack[0][p[2]] = {'classe': 'var',
                                                'endereco': p.parser.global_adress,
                                                'tamanho': [1],
                                                'tipo': p[1]}
            p.parser.global_adress += 1
            p.parser.local_adress += 1
        elif p[2] not in p.parser.id_table_stack[-1]:
            p.parser.id_table_stack[-1][p[2]] = {'classe': 'array',
                                                 'endereco': p.parser.local_adress,
                                                 'tamanho': [1],
                                                 'tipo': p[1]}
            p.parser.local_adress += 1
        else:
            print("ERROR : Variable %s already declared locally." % p[2],file=sys.stderr)
            p_error(p)


def p_declarray(p):
    "DeclArray : ID ID DeclArraySize"
    # int x[1][1][2]
    if p[1].lower() not in p.parser.type_table:
        print("ERROR: invalid type",file=sys.stderr)
    else:
        res = 1
        for s in p[3]:
            res *= s
        p[0] = f"pushn {res}\n"
        if len(p.parser.id_table_stack) == 1:
            p.parser.id_table_stack[0][p[2]] = {'classe': 'array',
                                                'endereco': p.parser.global_adress,
                                                'tamanho': p[3][1:],
                                                'tipo': p[1]}
            p.parser.global_adress += res
            p.parser.local_adress += res
        else:
            p.parser.id_table_stack[-1][p[2]] = {'classe': 'array',
                                                 'endereco': p.parser.local_adress,
                                                 'tamanho': p[3][1:],
                                                 'tipo': p[1]}
            p.parser.local_adress += res


def p_declarraysize_rec(p):
    "DeclArraySize : DeclArraySize '[' NUM ']'"
    p[0] = p[1]
    p[0].append(p[3])


def p_declarraysize_empty(p):
    "DeclArraySize : '[' NUM ']'"
    p[0] = [p[2]]


def p_atribarray_Leftatribop(p):
    "AtribArray : ID ArraySize LARROW AtribOp"
    for i in range(len(p.parser.id_table_stack)-1, 0, -1):
        if p[1] in p.parser.id_table_stack[i]:
            if p.parser.id_table_stack[i][p[1]]['classe'] == 'array':
                endereco = p.parser.id_table_stack[i][p[1]]['endereco']
                s = "pushfp\n"
                # tamanho nao guarda o primeiro!!"!"!!!!!""!"!"!"!"!"!"
                sizes = p.parser.id_table_stack[i][p[1]]['tamanho']
                break
            else:
                print("ERROR: Variable %s is not of array type" % p[1],file=sys.stderr)
                p_error(p)
    else:
        if p[1] in p.parser.id_table_stack[0]:
            if p.parser.id_table_stack[0][p[1]]['classe'] == 'array':
                endereco = p.parser.id_table_stack[0][p[1]]['endereco']
                s = "pushgp\n"
                # tamanho nao guarda o primeiro!!"!"!!!!!""!"!"!"!"!"!"
                sizes = p.parser.id_table_stack[0][p[1]]['tamanho']
            else:
                print("ERROR: Variable %s is not of array type" % p[1],file=sys.stderr)
                p_error(p)
        else:
            print("ERROR: Variable %s not in scope" % p[1],file=sys.stderr)
            p_error(p)
    if endereco != 0:
        s += f"pushi {endereco}\npadd\n"
    s += p[2]
    for size in sizes:
        s += f"pushi {size}\nmul\nadd\n"

    p[0] = s + p[4] + "storen\n"


def p_atribarray_Rightatribop(p):
    "AtribArray : AtribOp RARROW ID ArraySize"
    # 5+7 <--- x[2][5][4]
    # X[a][b][c]
    # X[x][y][z]
    # X + (x*c + y)*b + z
    # coloca o valor do atribop no topo da stack
    for i in range(len(p.parser.id_table_stack)-1, 0, -1):
        if p[3] in p.parser.id_table_stack[i]:
            s = "pushfp\n"
            # tamanho nao guarda o primeiro!!"!"!!!!!""!"!"!"!"!"!"
            sizes = p.parser.id_table_stack[i][p[3]]['tamanho']
            break
    else:
        if p[3] in p.parser.id_table_stack[0]:
            s = "pushgp\n"
            # tamanho nao guarda o primeiro!!"!"!!!!!""!"!"!"!"!"!"
            sizes = p.parser.id_table_stack[0][p[3]]['tamanho']
        else:
            print("ERROR: variable %s not in scope" % p[3],file=sys.stderr)
            return
    s += p[4]
    for size in sizes:
        s += f"pushi {size}\nmul\nadd\n"

    p[0] = s + p[1] + "storen\n"


def p_accessarray(p):
    "AccessArray : ID ArraySize"
    s = ""
    for i in range(len(p.parser.id_table_stack)-1, 0, -1):
        if p[1] in p.parser.id_table_stack[i]:
            end = p.parser.id_table_stack[i][p[1]]['endereco']
            sizes = p.parser.id_table_stack[i][p[1]]['tamanho']
            s += p[2]
            for size in sizes:
                s += f"pushi {size}\nmul\nadd\n"
            p[0] = f"pushfp\npushi {end}\npadd\n" + s + "loadn\n"
            return
    if p[1] not in p.parser.id_table_stack[0]:
        print("ERROR: Variable %s not in scope" % p[1],file=sys.stderr)
    else:
        end = p.parser.id_table_stack[0][p[1]]['endereco']
        sizes = p.parser.id_table_stack[0][p[1]]['tamanho']
        s += p[2]
        for size in sizes:
            s += f"pushi {size}\nmul\nadd\n"
        p[0] = f"pushgp\npushi {end}\npadd\n" + s + "loadn\n"
    return


def p_arraysize_rec(p):
    "ArraySize : ArraySize '[' AtribOp ']'"
    p[0] = p[3] + p[1]  # array nao ´e uma lista


def p_arraysize_empty(p):
    "ArraySize : '[' AtribOp ']'"
    p[0] = p[2]


def p_declatrib_left(p):
    "DeclAtrib : ID ID LARROW AtribOp"
    # int x <--------------------- 5+8
    if p[1].lower() not in p.parser.type_table:
        print("ERROR: invalid type",file=sys.stderr)
    else:
        p[0] = p[4]
        if len(p.parser.id_table_stack) == 1:
            p.parser.id_table_stack[0][p[2]] = {'classe': 'var',
                                                'endereco': p.parser.local_adress,
                                                'tamanho': [1],
                                                'tipo': p[1]}
            p.parser.global_adress += 1
            p.parser.local_adress += 1
        else:
            p.parser.id_table_stack[-1][p[2]] = {'classe': 'var',
                                                 'endereco': p.parser.local_adress,
                                                 'tamanho': [1],
                                                 'tipo': p[1]}
            p.parser.local_adress += 1


def p_declatrib_right(p):
    "DeclAtrib : AtribOp RARROW ID ID"
    # 7+5 -> int  INT Int iNt x? #####vao permitir isto???#####
    if p[3].lower() not in p.parser.type_table:
        print("ERROR: invalid type",file=sys.stderr)
    else:
        p[0] = p[1]
        if len(p.parser.id_table_stack) == 1:
            p.parser.id_table_stack[0][p[4]] = {'classe': 'var',
                                                'endereco': p.parser.global_adress,
                                                'tamanho': [1],
                                                'tipo': p[3]}
            p.parser.global_adress += 1
            p.parser.local_adress += 1
        else:
            p.parser.id_table_stack[-1][p[4]] = {'classe': 'var',
                                                 'endereco': p.parser.local_adress,
                                                 'tamanho': [1],
                                                 'tipo': p[3]}
            p.parser.local_adress += 1


def p_atribnum_left(p):
    "AtribNum : ID LARROW AtribOp"
    p[0] = p[3] + "dup 1\n" + gen_atrib_code_stack(p, p[1], p[3])


def p_atribnum_right(p):
    "AtribNum : AtribOp RARROW ID"
    # 2+4->x++
    p[0] = p[1] + "dup 1\n" + gen_atrib_code_stack(p, p[3], p[1])


def p_atribnum_array(p):
    "AtribNum : AtribArray"
    p[0] = p[1]


def p_atrib_left(p):
    "Atrib : ID LARROW AtribOp"
    p[0] = p[3] + gen_atrib_code_stack(p, p[1], p[3])


def p_atrib_right(p):
    "Atrib : AtribOp RARROW ID"
    p[0] = p[1] + gen_atrib_code_stack(p, p[3], p[1])


def p_atrib_equiv(p):
    "Atrib : ID SWAP ID"


    flag1 = flag2 = True
    
    for i in range(len(p.parser.id_table_stack)-1, 0, -1):

        if flag1 and p[1] in p.parser.id_table_stack[i]:
            end = p.parser.id_table_stack[i][p[1]]['endereco']
            end1 = "pushl %d\n" % end
            store1 = "storel %d\n" % end 
            flag1 = False
        if flag2 and p[3] in p.parser.id_table_stack[i]:
            end = p.parser.id_table_stack[i][p[3]]['endereco']
            end2 = "pushl %d\n" % end
            store2 = "storel %d\n" % end 
            flag2 = False
        if not (flag1 or flag2):
            p[0] = end1 + end2 + store1 + store2
            return

    if flag1:
        if p[1] in p.parser.id_table_stack[0]:
            end = p.parser.id_table_stack[0][p[1]]['endereco']
            end1 = "pushg %d\n" % end
            store1 = "storeg %d\n" % end 
        else:
            print("ERROR: Variable %s not in scope" % p[1],file=sys.stderr)    
    if flag2: 
        if p[3] in p.parser.id_table_stack[0]:
            end = p.parser.id_table_stack[0][p[3]]['endereco']
            end2 = "pushg %d\n" % end
            store2 = "storeg %d\n" % end 
        else:
            print("ERROR: Variable %s not in scope" % p[3],file=sys.stderr)
    
    p[0] = end1 + end2 + store1 + store2

    return


def p_atrib_array(p):
    "Atrib : AtribArray"
    p[0] = p[1]


# def p_op_opuno(p):
#    "Op : OpUno"
#    p[0] = p[1]


def p_op_opbin(p):
    "Op : OpBin"
    p[0] = p[1]


def p_opuno_neg(p):
    "OpUno : NEG Base"
    p[0] = p[2] + 'not\n'


def p_opuno_accessarray(p):
    "OpUno : AccessArray"
    p[0] = p[1]


def p_opuno_minus(p):
    "OpUno : SUB Base"
    p[0] = "pushi 0\n" + p[2] + "sub\n"


def p_opuno_print(p):
    "OpUno : Base PRINT"
    # funciona para tudo que não seja array
    p[0] = p[1] + "dup 1\n" + "writei\n" + r'pushs "\n"' + "\nwrites\n"



def p_opbin_rec(p):
    "OpBin : OpBin OpLogico TermMod"
    p[0] = p[1] + p[3] + p[2]


def p_opbin_base(p):
    "OpBin : TermMod"
    p[0] = p[1]


def p_opmod_rec(p):
    "TermMod : TermMod OpMod TermPlus"
    p[0] = p[1] + p[3] + p[2]


def p_opmod_base(p):
    "TermMod : TermPlus"
    p[0] = p[1]


def p_termplus_rec(p):
    "TermPlus : TermPlus OpPlus TermMult"
    p[0] = p[1] + p[3] + p[2]


def p_termplus_base(p):
    "TermPlus : TermMult"
    p[0] = p[1]


def p_termmult_rec(p):
    "TermMult : TermMult OpMult TermPow"
    p[0] = p[1] + p[3] + p[2]


def p_termmult_base(p):
    "TermMult : TermPow"
    p[0] = p[1]


def p_termpow_rec(p):
    "TermPow : TermPow OpPow Base"
    p[0] = p[1] + p[3] + p[2]


def p_termpow_base(p):
    "TermPow : Base"
    p[0] = p[1]


def p_base_opuno(p):
    "Base : OpUno"
    p[0] = p[1]


def p_base_exp(p):
    "Base : '(' AtribOp ')'"
    p[0] = p[2]


def p_base_id(p):
    "Base : ID"
    for i in range(len(p.parser.id_table_stack)-1, 0, -1):
        if p[1] in p.parser.id_table_stack[i]:
            p[0] = "pushl %d\n" % p.parser.id_table_stack[i][p[1]]['endereco']
            return
    if p[1] not in p.parser.id_table_stack[0]:
        print("ERROR: variable %s not in scope" % p[1],file=sys.stderr)
        p_error(p)
    else:
        p[0] = "pushg %d\n" % p.parser.id_table_stack[0][p[1]]['endereco']
    return


def p_base_num(p):
    "Base : NUM"
    p[0] = "pushi %d\n" % p[1]


def p_base_funcall(p):
    "Base : FunCall"
    if (p[1][1]):
        p[0] = p[1][0]
    else:
        print("ERROR: Function %s doesn't return any value" % p[1][2] +
              " and is used in an operation.",file=sys.stderr)
        p_error(p)


def p_base_read(p):
    "Base : READ"
    p[0] = "read\natoi\n"


def p_funcall(p):
    "FunCall : ID '(' FunArg ')'"
    # print(p.parser.function_table)
    if p[1] not in p.parser.function_table:
        print("ERROR: Function %s not defined" % p[1],file=sys.stderr)
        p_error(p)
    label = p.parser.function_table[p[1]]['label']
    var_num = p.parser.function_table[p[1]]['num_args']
    if var_num == len(p[3]):
        p[0] = ("".join(p[3]) +
                f"pusha {label}\n" +
                "call\n" +
                f"pop {var_num-int(p.parser.function_table[p[1]]['return'])}\n",
                p.parser.function_table[p[1]]['return'],
                p[1])  # Nao esquecer de por o return em cima da primeira variavelF
    else:
        print("ERROR: Number of arguments given %d is not equal to needed %d, for function %s"
              % (len(p[3]), var_num, p[1]),file=sys.stderr)
        p_error(p)


def p_funarg_funrec(p):
    "FunArg : FunRec"
    p[0] = p[1]


def p_funarg_empty(p):
    "FunArg : "
    p[0] = []


def p_funrec_rec(p):
    "FunRec : FunRec ',' AtribOp"
    p[0] = p[1]
    p[0].append(p[3])


def p_funrec_base(p):
    "FunRec : AtribOp"
    p[0] = [p[1]]


def p_oplogico_diff(p):
    "OpLogico : DIFF"
    p[0] = "equal\nnot\n"

def p_oplogico_and(p):
    "OpLogico : AND"
    p[0] = "and\n"


def p_oplogico_or(p):
    "OpLogico : OR"
    p[0] = "or\n"


def p_oplogico_lesser(p):
    "OpLogico : LESSER"
    p[0] = "inf\n"


def p_oplogico_greater(p):
    "OpLogico : GREATER"
    p[0] = "sup\n"


def p_oplogico_leq(p):
    "OpLogico : LEQ"
    p[0] = "infeq\n"


def p_oplogico_geq(p):
    "OpLogico : GEQ"
    p[0] = "supeq\n"


def p_oplogico_equal(p):
    "OpLogico : EQUAL"
    p[0] = "equal\n"

def p_opmod_mod(p):
    "OpMod : MOD"
    p[0] = "mod\n"

def p_opplus_add(p):
    "OpPlus : ADD"
    p[0] = "add\n"


def p_opplus_sub(p):
    "OpPlus : SUB"
    p[0] = "sub\n"


def p_opmult_mul(p):
    "OpMult : MUL"
    p[0] = "mul\n"


def p_opmult_div(p):
    "OpMult : DIV"
    p[0] = "div\n"


def p_oppow(p):
    "OpPow : POW"

    fp_pow = open("pow.vm", "r")  # retorna erro se ficheiro nao existir

    pow_function_string = fp_pow.read()

    if p.parser.pow_flag:
        # adiciona ao buffer mas nao ´a tabela
        p.parser.function_buffer.append(pow_function_string)
        p.parser.pow_flag = False
    p[0] = "pusha P\ncall\npop 1\n"


def p_error(p):
    print("Syntax error!")
    # print(p)
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State: {} {}\n . {}\n'
          .format(parser.state,
                  stack_state_str,
                  p))
    raise SyntaxError


# eu pus este codigo aqui em baixo para nao misturar
# as cenas da gramatica com outro codigo


def gen_atrib_code_stack(p, id, atribop):
    s = ""
    for tamanho in range(len(p.parser.id_table_stack)-1, 0, -1):
        if id in p.parser.id_table_stack[tamanho]:
            s = "storel %d\n" % p.parser.id_table_stack[tamanho][id]['endereco']
            break
    else:
        if id not in p.parser.id_table_stack[0]:
            print("ERROR: Name %s not defined." % id,file=sys.stderr)
            # invoke error
        else:
            s = "storeg %d\n" % p.parser.id_table_stack[0][id]['endereco']
    return s


def pop_local_vars(p):
    s = ""
    min = float("inf")
    pop_size = 0
    for var in p.parser.id_table_stack[-1]:
        pop_size += prod(p.parser.id_table_stack[-1][var]['tamanho'])
        if (n := p.parser.id_table_stack[-1][var]['endereco']) < min:
            min = n
    if min != float("inf"):
        p.parser.local_adress = min
    s += "pop %d\n" % pop_size
    p.parser.id_table_stack.pop()
    return s


parser = yacc.yacc(debugfile="yacc.debug")

# 0->global; 1+->local
# ++ x = (tipo, classe, localidade, endereço, dimenção)
parser.main = False
parser.type_table = {'int'}
parser.id_table_stack = list()
parser.id_table_stack.append(dict())
parser.label_table_stack = list()  # isto vai ser uma lista de pares
parser.function_table = dict()
parser.pow_flag = True  # leia-se ´e preciso por o texto do pow? Devia começar a false?
parser.internal_label = 0
parser.global_adress = 0
parser.local_adress = 0
parser.function_buffer = []
parser.final_code = ""
# a ideia era a cond ter [label:cond ...] e a case ter [lable:body ...]
# ambas tem uma chave special ":" onde pomos numa lista todas as conds e bodies sem lables
# na label_table_stack podemos por o par

file_in = input()

f = open(file_in, "r")
ligma_code = f.read()

parser.parse(ligma_code, debug=1)

f.close()

#f = open("test1.vm", "w")
# f.write(parser.final_code)

print(parser.final_code)
