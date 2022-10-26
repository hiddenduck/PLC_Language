import re

print("Split de uma linha por virgulas")

input = open("emd.csv", "r", encoding="utf-8")
entradas = {}
i = 0
for linha in input:
    entradas[i] = re.split(r',', linha)
    i+=1
input.close()
output = open("output.txt", "w")
for i in entradas:
    output.write(str(entradas[i]) + "\n")
print(entradas)