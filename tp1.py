import re
import time

def teste1(l):
    return [[x] for x in l]

start = time.time()
colunas = []

input = open("teste2.csv", "r", encoding="utf-8")
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?', primeira)
print(colunas)
#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for

res = '[\n'
#0->título, 1->min, 2->max, 3->fun
for linha in input:
    linha = re.sub(r'\n$', r'', linha)
    split = re.split(r',', linha)
    r = 0 #ponto da lista split a ler
    res += '\t{\n'
    for i in range(len(colunas)):
        if colunas[i][1] == '':
            res += '\t\t\"%s\": \"%s\",\n' % (colunas[i][0], split[r])
            r += 1
        else:
            max = int(colunas[i][1]) if colunas[i][2] == "" else int(colunas[i][2])
            lis = []
            for l in range(max):
                if split[r] != '':
                    lis.append((split[r]))
                r+=1
            if colunas[i][3] == '':
                res+='\t\t\"%s\": %s,\n' % (colunas[i][0], str(lis))
            else:
                fun = eval(colunas[i][3])
                res+='\t\t\"%s_%s\": %s,\n' % (colunas[i][0], colunas[i][3], str(fun(map(int,lis))))
    res = re.sub(r',\n$', '\n\t},\n', res) #res[:-2] + '\n\t},\n'
res = re.sub(r',\n$', '\n]', res) #res[:-2] + '\n]'
print(res)

end = time.time()

print("time: %d ms" % ((end-start)*1000))
input.close()
