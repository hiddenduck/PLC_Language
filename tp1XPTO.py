import re
import time

start = time.time()

def teste1(lista):
    return [[x] for x in lista]

colunas = []

filename = "teste1.csv"

input = open(filename, "r", encoding="utf-8")
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(\d+)(?:,(\d+))?})?(?:::([^,]+))?', primeira)

#será que é possível fazer sub(ou mesmo sub n) nesta string e construir logo algo super interessante, uma linha magica logo de estoura, evitando um for
#print(colunas)

patern = r''
replace = r'\t{\n'
fun_str = r''
i = 1
#colunas: 0 -> título; 1->min/único; 2->max; 3->função
for coluna in colunas:
    if coluna[1] == '':
        patern += r'([^{,]+),'    
        replace += r'\t\t"%s": "\%d",\n' % (coluna[0],i)
    else:
        min = int(coluna[1])
        max = min
        if coluna[2] != '':
            max = int(coluna[2])
        patern += r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},' % (min-1, max-1, max - min)
        if coluna[3] != '':
            fun_str += r'%s|' % (coluna[3])
            replace += r'\t\t"%s_%s": %s([\%d]),\n' % (coluna[0],coluna[3],coluna[3],i)
        else:
            replace += r'\t\t"%s": [\%d],\n' % (coluna[0],i)
    i += 1

patern = patern[:-1]
replace = replace [:-3] + "\n\t},\n"
fun_str = fun_str[:-1]
#print(patern)
#print(replace)
#o group de 0 é a linha sempre?

res = '[\n'
for linha in input:
    linha = linha[:-1]
    #print(linha)
    res += re.sub(patern,replace,linha)
    
res = re.sub(r'(((?:%s))\(.*\))'%(fun_str), lambda x: str(eval(x.group(1))),res)
res = res[:-2] + "\n]"

print(res)

end = time.time()

print("time: %d ms" % ((end-start) * 1000))

input.close()

filename = re.sub(r'.csv',r'.json',filename)

output = open(filename, 'w', encoding="utf-8")
output.write(res)
output.close()
