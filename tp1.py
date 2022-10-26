import re

print("Split de uma linha por virgulas")

input = open("emd.csv", "r", encoding="utf-8")
entradas = {}
entradas[0] = re.split(r'\,(?!s*[0-9]+})',linha[0:-1])
for i,linha in enumerate(input[1:]):
    linha = linha[:-1]
     entradas[i+1] = re.split(r',', linha)
input.close()
output = open("output.txt", "w")
for i in entradas:
    output.write(str(entradas[i]) + "\n")
print(entradas)
