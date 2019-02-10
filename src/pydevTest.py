a = ['mary','has','a','little','lamb']
for i in range(0,len(a),2):
    print(i,a[i])
    
for x in a[:]:
    if len(x)>3: a.insert(0,x)
    
print(a)

print(list(range(5,10)))

for n in range(2,10):
    for x in range(2,n):
        if n%x==0:
            print(n,'equals',x,'x',n//x)
            break
    else:
        print(n,'is a prime number')
         
class MyEmptyClass:
    pass

def fib(n):
    """返回直到n的Fibonacci数列"""
    result=[]
    a,b=0,1
    while a<n:
        result.append(a)
        a,b=b,a+b
    return result
    
f=fib
print(f(200))

def fap(a,L=[]): #默认参数只赋值一次
    L.append(a)
    return L

print(fap(1))
print(fap(2))

vec =[2,4,6]
vect=[[x,x**2] for x in vec if x>3] #列表推导式
print(vect)

a=set('abacadaeaf') #集合
b={'a','b','b','g','z'}
print(a,b)
print(a-b)

tel={'jack':4098, 'sape':4139} #字典
tel['guido']=4127
print(list(tel.keys()))
print(sorted(tel.keys()))
print('guido' in tel)
table=[(x,y**2) for x,y in zip('abc', reversed([2,4,6]))]
d=dict(table)
for k,v in d.items():
    print(k,v)

import sys
print(sys.path)





