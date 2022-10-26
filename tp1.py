import re

print("Split de uma linha por virgulas")

input = open("emd.csv", "r", encoding="utf-8")
entradas = []
entradas.append(re.split(r'\,(?!s*[0-9]+})', input.readline())) 

for linha in input:
    linha = linha[:-1]
    entradas.append(re.split(r',', linha))
input.close()
output = open("output.txt", "w")
for i in range(len(entradas)):
    output.write(str(entradas[i]) + "\n")
print(entradas)
