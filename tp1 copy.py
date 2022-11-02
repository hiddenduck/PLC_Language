import re

colunas = []

print("Split de uma linha por virgulas")

input = open("teste1.csv", "r", encoding="utf-8")
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?', primeira)
#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for
print(colunas)

linha_magica = r''
lm = lambda x: ''
print(linha_magica)
i = 1
#colunas: 0 -> título; 1->min/único; 2->max; 3->função
for coluna in colunas:
    if coluna[1] != '':
        #será possível escrever esta restrição sem obrigar que exista pelo menos um, para podermos usar 0
        if coluna[2] == '':
            coluna[2] = coluna[1]
            #tentar evitar as vírgulas com espaços vazios porque torna o resto muito mais fácil
        #apanha os casos todos logo, também só aumenta 5 bytes a cada string?
        linha_magica += r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},' % (int(coluna[1])-1, int(coluna[2])-1,int(coluna[2]) - int(coluna[1]))
    else:
        linha_magica += r'([^{,]+),'
linha_magica = linha_magica[:-1]
print(linha_magica)
print(lm)
#o group de 0 é a linha sempre?

res = ''
for linha in input:
    linha = linha[:-1]
    for coluna in colunas:
        if coluna[1] != '':
            if coluna[2] != '':
                if coluna[3] != '':
                    fun = eval(coluna[3])
                    linha = re.sub(r'([^,]+(?:,[^,]+){%d,%d})' % (int(coluna[1])-1, int(coluna[2])-1), r'%s_%s:\11111\n' % (coluna[0],coluna[3]), linha, count = 1)
                    break    
                linha = re.sub(r'([^,]+(?:,[^,]+){%d,%d})' % (int(coluna[1])-1, int(coluna[2])-1), (r'%s:[\1]2222222\n' % coluna[0]), linha, count = 1)
                break
        linha = re.sub(r'([^,]+(?:,[^,]+))', r'%s:\1333333333\n'%coluna[0], linha, count = 1)
    res += linha
    print(linha)
#print(res)

input.close()














d = {
    [3,2,1],
    [3,2,1],
    [3,2,1,4,5,6,7],
    [3,2,1],
    [1,2,3],
    [1,2,3],
}

