import random

allIngredient = range(1100) # 50-1049 are used with a probability

classes = []
for i in range(1,11): # 10 commodity classes
    instances = []
    for j in range(100): # 100 commodities in each class
        commodity = set()
        for r in range(12): # each commodity contains at most 12 ingredients of which 2 are not allowed
            if r<10:
                commodity.add(random.randint(i*100-50,i*100+49)) # allowed ingredients, for class 1, no50-no149
            else:
                commodity.add(random.randint(i*100+50,i*100+99)) # ingredients not allowed, for class1, no150-no199
        instances.append(commodity)
    classes.append(instances)

o = open('C:/facts/commodities.csv', 'w')    
d = 0
for i in classes:
    d+=1
    for j in i:
        o.write(str(d))
        for f in j:
            o.write(','+str(f))
        o.write('\n')
        
i = open('C:/facts/commodities.csv', 'r')
commodities = []
lines = i.read().split('\n')
for line in lines:
    cla = line.split(',')[0]
    igr = line.split(',')[1:]
    commodities.append((cla,igr))
    
for c in commodities:
    print(c)
    

