import re

print("Split de uma linha por virgulas")

input = open("teste1.csv", "r")
entradas = {}
i = 0
for linha in input:
    entradas[i] = re.split(r',', linha)
    i+=1
input.close()
print(entradas)