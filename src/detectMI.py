import math
import operator

o = open('C:/facts/commodities-noID.csv', 'r') 
dfs = {} #{'0':0}
coTable = {} #{('0','0'):0.0}
lines = o.read().split('\n')
commodities = []
for l in lines:
    c = l.split(',')
    commodities.append(c)
    for x in c:
        if x in dfs.keys():
            dfs[x] += 1
        else:
            dfs[x] = 1
        for y in c:
            if (x,y) in coTable.keys():
                coTable[(x,y)] += 1.0
            else:
                coTable[(x,y)] = 1.0
            
o.close()
for k,v in coTable.items():
    #print(k,dfs[k[0]],dfs[k[1]])
    d = v*len(lines)/(dfs[k[0]]*dfs[k[1]]);
    coTable[k] = math.log(d)

t = 1
for g in coTable:
    print(g,coTable[g])
    t += 1
    if t > 10:
        break

predict_vs_real = []
TP = 0 # True positive
APP = 0 # All predicted positive
ARP = 0 # All real positive
for c in range(len(commodities)):
    predrisk = []
    realrisk = []
    miAvrList = {} #{'0':0.0}
    for x in c:
        miSum = 0
        for y in c:
            miSum += coTable[(x,y)]
        miAvr = miSum/len(c)
        miAvrList[x] = miAvr
        miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1))
        for n in range(2):
            predrisk.append(miAvrRank[n][0])
        
        
        
        
        