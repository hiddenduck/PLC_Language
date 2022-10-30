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
    if s.group(3):
        max = int(s.group(3))
    return r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},' % (min-1, max-1, max - min)

linha_magica = re.sub(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?,*', linha_magica_constructor, primeira)
linha_magica = linha_magica[:-1]
print(linha_magica)

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