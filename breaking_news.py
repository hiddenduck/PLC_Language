# %% [markdown]
# Let'sa GO!
# # Processamento de Linguagens e Compiladores
# ## Trabalho Prático 1 - Relatório
# 
# André Lucena Ribas Ferreira (A94956)
# 
# Carlos Edurdo da Silva Machado (A96936)
# 
# Gonçalo Manuel Maia de Sousa (A97485)

# %% [markdown]
# Utilizaremos o módulo 're' que oferece operações de matching de expressões regulares em python.

# %%
import re
from pprint import pprint

# %% [markdown]
# Obtemos o ficheiro de input do utilizador

# %%
filename = 'teste1.csv'#input("introduza o ficheiro de input:")
input = open(filename, "r", encoding="utf-8")

# %% [markdown]
# 

# %%
primeira = input.readline()[:-1]
colunas = re.findall(r'(?<![^,])([^{^,]+)(?:{(?:(\d+),)?(\d+)})?(?:::([^,]+))?', primeira)
pprint(colunas)

# %% [markdown]
# 

# %%
patern = fun_str = r''
replace = '\t{\n'

# %% [markdown]
# 

#colunas: 0 -> título; 1->min/único; 2->max; 3->função
for i,coluna in enumerate(colunas, start=1):
    if coluna[2] == '':
        patern += r'([^{,]+),'    
        replace += '\t\t"%s": "\%d",\n' % (coluna[0],i)
    else:
        max = int(coluna[2])
        min = max if coluna[1] == '' else int(coluna[1])
        patern += r'([^,]+(?:,[^,]+){%d,%d}),{0,%d},' % (min-1, max-1, max - min)
        if coluna[3] != '':
            fun_str += r'%s|' % (coluna[3])
            replace += '\t\t"%s_%s": %s([\%d]),\n' % (coluna[0],coluna[3],coluna[3],i)
        else:
            replace += '\t\t"%s": [\%d],\n' % (coluna[0],i)

patern = patern[:-1]
replace = re.sub(r',\n$', '\n\t},\n', replace) #replace = replace[:-2] + '\n\t},\n'
fun_str = fun_str[:-1]

print(patern)
print(replace)


res = '[\n'
for linha in input:
    linha = linha[:-1]
    #print(linha)
    res += re.sub(patern,replace,linha)

res = re.sub(r'(((?:%s))\(.*\))'%(fun_str), lambda x: str(eval(x.group(1))),res)
res = re.sub(r',\n$', '\n]', res)#res = res[:-2] + "\n]"

# %% [markdown]
# 

# %%
input.close()

filename = re.sub(r'csv',r'json',filename)

output = open(filename, 'w', encoding="utf-8")

print(res) #remover depois ou não 

output.write(res)
output.close()

# %%



