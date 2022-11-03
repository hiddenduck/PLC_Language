import re







f1 = eval("sum([1,2,3,4,5])")
#f2 = eval("mean")

print(f1)
#print(f2)

l = []
l.append(f1)
#l.append(f2)

i = 0

def fun(i,line):
    return str(l[i](map(int,re.split(r',',line))))


line = '[1,2],[3,4]'

line = re.sub(r'(1,2)',lambda x: fun(i,x.group(1)) ,line)


print(line)





















