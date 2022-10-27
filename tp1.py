import re

colunas = []

print("Split de uma linha por virgulas")

input = open("teste1.csv", "r", encoding="utf-8")
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?', input.readline()[:-1])
#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for
print(colunas)

linha_magica = r''

#colunas: 0 -> título; 1->min/único; 2->max; 3->função
for coluna in colunas:
    if coluna[1] != '':
        #será possível escrever esta restrição sem obrigar que exista pelo menos um, para podermos usar 0
        if coluna[2] != '':
            #tentar evitar as vírgulas com espaços vazios porque torna o resto muito mais fácil
            linha_magica += r'([^,]+(?:,[^,]+){%d,%d}),{1,%d}' % (int(coluna[1])-1, int(coluna[2])-1,int(coluna[2]) - int(coluna[1]) + 1)
            #min e max
        else:
            linha_magica += r'([^,]*(?:,[^,]*){%d}),' % (int(coluna[1])-1)
            #único
        #no matching não preciso de fazer nada para a função
    else:
        linha_magica += r'([^{,]+),'
linha_magica = linha_magica[:-1]
print(linha_magica)
#o group de 0 é a linha sempre?
for linha in input:
    print(linha)
    teste = re.search(linha_magica, linha)
    for i in range(len(colunas)):
        if (colunas[i][1] == ''):
            lista = re.split(r',', teste.group(i+1))
            if (colunas[i][3] != ''):
                fun = eval(colunas[i][3])
                print(colunas[i][0] + "_" + colunas[i][3] + " : " + str(fun(map(int,lista))))
            else:
                print(colunas[i][0] + " : " + str(lista))
        else:
            print(colunas[i][0] + " : " + teste.group(i+1))

input.close()
