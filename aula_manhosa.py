import re

input = open("entrevista.txt", 'r', encoding='utf-8')

nomes = ['Entrevistador', 'Entrevistado']

res = ''

def fun(nomes, s):
    if s.group(1):
        return nomes[0] + ': '
    elif s.group(2):
        nomes[0] = s.group(2)
        return ""
    elif s.group(3):
        return nomes[1] + ': '
    else:
        nomes[1] = s.group(4)
        return ""

for linha in input:
    linha = re.sub(r'^(?i)(eu\s?):\s?|^(?i)eu\s?=\s?([^.]+)\.?\n?|^(?i)(ele\s?):\s?|^(?i)ele\s?=\s?([^.]+)\.?\n?',lambda x: fun(nomes, x) ,linha)
    """linha = re.sub(r'^(?i)eu\s?:\s?', nomes[0]+': ', linha)
    match = re.search(r'^(?i)eu\s?=\s?([^.]+)', linha)
    if match:
        nomes[0] = match.group(1)
    linha = re.sub(r'^(?i)ele\s?:\s?', nomes[1]+': ', linha)
    match = re.search(r'^(?i)ele\s?=\s?([^.]+)', linha)
    if match:
        nomes[1] = match.group(1)"""
    res += linha

print(res)