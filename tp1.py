import re

colunas = []
entrada = []

print("Split de uma linha por virgulas")

input = open("emd.csv", "r", encoding="utf-8")
colunas = re.split(r'\,(?!\s*[0-9]+})', input.readline()[:-1])
print(colunas)

for linha in input:
    escrita = {}
    r = 0
    entrada = (re.split(r',', linha[:-1]))
    for i in range(len(colunas)):
        l = re.search(r'{\d+(\,\d+)?}', colunas[i])
        if l:
            print("listas")
            #lidar com listas
        else:
            escrita[]

    print(entrada)
input.close()
