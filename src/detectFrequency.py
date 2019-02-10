import operator

i = open('C:/facts/commodities.csv', 'r')
commodities = []
lines = i.read().split('\n')
for line in lines:
    cla = line.split(',')[0]
    igr = line.split(',')[1:]
    commodities.append((cla,igr))
    
tfidf = []
for c in commodities:
    voc = [0 for n in range(1100)]
    for i in c[1]:
        voc[int(i)] = 1
    tfidf.append(voc)
        
frequency = dict([(n,0) for n in range(1100)])
for m in tfidf:
    for x in range(1100):
        frequency[x] = frequency[x] + m[x]
sorted_f = sorted(frequency.items(), key=operator.itemgetter(1))
thred = 300
b = 0
risks = [] # ingredients with frequency = 0 + the 300 most rarely appeared ingredients with frequency > 0
for g in sorted_f:
    if g[1] == 0:
        risks.append(g[0])
    elif b < thred:
        risks.append(g[0])
        b += 1
        
print(risks)
    
predict_vs_real = []
TP = 0 # True positive
APP = 0 # All predicted positive
ARP = 0 # All real positive
for m in range(len(tfidf)):
    predrisk = []
    realrisk = []
    for e in range((int(m/100)+1)*100+50,(int(m/100)+1)*100+100):
        if tfidf[m][e] > 0:
            realrisk.append(e)
    for r in risks:
        if tfidf[m][r] > 0:
            predrisk.append(r)
    predict_vs_real.append((predrisk,realrisk))
    ARP += len(realrisk)
    for pr in predrisk:
        APP += 1
        if pr in realrisk:
            TP += 1
    print(m,(predrisk,realrisk))
          
print('Precision =',str(TP/APP))
print('Recall =',str(TP/ARP))


    
