import re
import time

def teste1(l):
    return [[x] for x in l]

start = time.time()
colunas = []

print("Split de uma linha por virgulas")

input = open("emd.csv", "r", encoding="utf-8")
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?', primeira)
#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for

res = '[\n'
#0->título, 1->min, 2->max, 3->fun
for linha in input:
    linha = linha[:-1]
    split = re.split(r',', linha)
    r = 0
    res += '\t{'
    for i in range(len(colunas)):
        if colunas[i][1] == '':
            res += ',\n\t\t\"%s\": \"%s\"' % (colunas[i][0], split[r])
            r += 1
        else:
            max = int(colunas[i][1])
            if colunas[i][2] != '':
                max = int(colunas[i][2])
            lis = []
            for l in range(max):
                if split[r] != '':
                    lis.append((split[r]))
                r+=1
            if colunas[i][3] == '':
                res+=',\n\t\t\"%s\": %s' % (colunas[i][0], str(lis))
            else:
                fun = eval(colunas[i][3])
                res+=',\n\t\t\"%s_%s\": %s' % (colunas[i][0], colunas[i][3], str(fun(map(int,lis))))
    res += '\n\t}\n'
res = res + ']'
#print(res)

end = time.time()

print("time: %d ms" % ((end-start)*1000))
input.close()
