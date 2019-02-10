from sklearn.cluster import KMeans
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
    
km = KMeans(n_clusters=10)
clusters = km.fit_predict(tfidf)
types = set(clusters) #class labels

classes = []
for c in types:
    clustered = []
    for d in range(1000):
        if clusters[d] == c:
                clustered.append((d,tfidf[d]))
    classes.append(clustered)

risky = []
for cluster in classes: # find risky ingredients for each class
    frequency = dict([(n,0) for n in range(1100)])
    for m in cluster:
        for x in range(1100):
            frequency[x] = frequency[x] + m[1][x]
    sorted_f = sorted(frequency.items(), key=operator.itemgetter(1))
    thred = 30
    b = 0
    risks = [] # ingredients with frequency = 0 + the 30 most rarely appeared ingredients with frequency > 0
    for g in sorted_f:
        if g[1] == 0:
            risks.append(g[0])
        elif b < thred:
            risks.append(g[0])
            b += 1
    risky.append(risks)
    print(risks)
    
predict_vs_real = []
TP = 0 # True positive
APP = 0 # All predicted positive
ARP = 0 # All real positive
for l in range(len(classes)):
    cluster = classes[l]
    risks = risky[l]
    for m in cluster: # m = (d,tfidf[d])
        predrisk = []
        realrisk = []
        for e in range((int(m[0]/100)+1)*100+50,(int(m[0]/100)+1)*100+100):
            if m[1][e] > 0:
                realrisk.append(e)
        for r in risks:
            if m[1][r] > 0:
                predrisk.append(r)
        predict_vs_real.append((predrisk,realrisk))
        ARP += len(realrisk)
        for pr in predrisk:
            APP += 1
            if pr in realrisk:
                TP += 1
        print(m[0],(predrisk,realrisk))
        
print('Precision =',str(TP/APP))
print('Recall =',str(TP/ARP))


    
