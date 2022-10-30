import re

colunas = []

print("Split de uma linha por virgulas")

input = open("teste1.csv", "r", encoding="utf-8")
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?,*', primeira)
print(colunas)

def linha_magica_constructor(s):
    print(s)
    if not s.group(2):
        return r'([^{,]+),'
    min = int(s.group(2))
    max = min
    fun = ""
    if s.group(3):
        max = int(s.group(3))
    if s.group(4):
        fun = s.group(4)
    return r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},(%s){0}' % (min-1, max-1, max - min, fun)

linha_magica = re.sub(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?,*', linha_magica_constructor, primeira)
linha_magica = linha_magica[:-1]
print(linha_magica)
#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for

#colunas: 0 -> título; 1->min/único; 2->max; 3->função
#for coluna in colunas:
#    if coluna[1] != '':
#        #será possível escrever esta restrição sem obrigar que exista pelo menos um, para podermos usar 0
#        if coluna[2] == '':
#            coluna[2] = coluna[1]
#            #tentar evitar as vírgulas com espaços vazios porque torna o resto muito mais fácil
#        #apanha os casos todos logo, também só aumenta 5 bytes a cada string?
#        linha_magica += r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},' % (int(coluna[1])-1, int(coluna[2])-1,int(coluna[2]) - int(coluna[1]))
#    else:
#        linha_magica += r'([^{,]+),'
#linha_magica = linha_magica[:-1]
#print(linha_magica)
#print(linha_magica == result)

#o group de 0 é a linha sempre?
for linha in input:
    linha = linha[:-1]
    print(linha)
    teste = re.search(linha_magica, linha)
    for i in range(len(colunas)):
        if (colunas[i][1] != ''):
            lista = re.split(r',', teste.group(i+1))
            if (colunas[i][3] != ''):
                fun = eval(colunas[i][3])
                print(colunas[i][0] + "_" + colunas[i][3] + " : " + str(fun(map(int,lista))))
            else:
                print(colunas[i][0] + " : " + str(lista))
        else:
            print(colunas[i][0] + " : " + teste.group(i+1))

input.close()
