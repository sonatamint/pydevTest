import random
import operator
import math
from sklearn.cluster import KMeans
from gensim.models import word2vec

#vocabulary_length = 1100

def dataGeneration(topath = 'C:/facts/commoditiesN.csv'):
    classes = []
    for i in range(1,11): #10 commodity classes
        instances = []
        for j in range(100): #100 commodities in each class
            commodity = set()
            for r in range(12): #each commodity contains at most 12 ingredients of which 2 are not allowed
                if r<10:
                    commodity.add(random.randint(i*100-50,i*100+49)) #allowed ingredients, for class 1, no.50-no.149
                else:
                    commodity.add(random.randint(i*100+50,i*100+99)) #ingredients not allowed, for class 1, no.150-no.199
            instances.append(commodity)
        classes.append(instances)
    o = open(topath, 'w')
    s = ''    
    d = 0
    for i in classes:
        d+=1
        for j in i:
            s += str(d) #o.write(str(d))
            for f in j:
                s += ','+str(f) #o.write(','+str(f))
            s += '\n' #o.write('\n')
    o.write(s.strip('\n'))
    o.close()
    return classes

def detectRiskByVectorDist(classified = [], frompath = 'C:/facts/commoditiesN.csv'):
    commodities = []
    if len(classified)>0:
        i = open('C:/facts/text8text', 'w')
        d = 0
        for c in classified:
            d+=1
            for j in c:
                #cla = str(d)
                igr = []
                for f in j:
                    igr.append(str(f))
                    i.write(str(f)+' ')
                commodities.append(igr)
                i.write('\n')
        i.close()
    else:
        i = open(frompath, 'r')
        content = i.read()
        lines = content.split('\n')
        o = open('C:/facts/text8text', 'w')
        modified = content.replace(',',' ')
        o.write(modified)
        o.close()
        for line in lines:
            #cla = line.split(',')[0]
            igr = line.split(',')[1:]
            commodities.append(igr)
        i.close()
        
    sentences=word2vec.Text8Corpus('C:/facts/text8text')
    model=word2vec.Word2Vec(sentences,min_count=1,size=50)
    #print(100,model['100'])
    predict_vs_real = {}
    TP = 0 # True positive
    APP = 0 # All predicted positive
    ARP = 0 # All real positive
    for l in range(len(commodities)):
        igr = commodities[l]
        predrisk = []
        realrisk = []
        for e in range((int(l/100)+1)*100+50,(int(l/100)+1)*100+100):
            if str(e) in igr:
                realrisk.append(str(e))
        ARP += len(realrisk)
        p1 = model.doesnt_match(igr)
        predrisk.append(p1)
        igr.remove(p1)
        p2 = model.doesnt_match(igr)
        predrisk.append(p2)
        for pr in predrisk:
            APP += 1
            if pr in realrisk: 
                TP += 1
        predict_vs_real[l] = [predrisk,realrisk]
        #print(l, (predrisk,realrisk))
        
    print('Precision =',str(TP/APP))
    print('Recall =',str(TP/ARP))
    return predict_vs_real

def detectRiskByMutualInfo(classified = [], frompath = 'C:/facts/commoditiesN.csv'):
    commodities = []
    dfs = {} #{'0':0}
    coTable = {} #{('0','0'):0.0}
    if len(classified)>0:
        d = 0
        for i in classified:
            d+=1
            for j in i:
                #cla = str(d)
                igr = []
                for f in j:
                    igr.append(str(f))
                commodities.append(igr)
    else:
        i = open(frompath, 'r')
        lines = i.read().split('\n')
        for line in lines:
            #cla = line.split(',')[0]
            igr = line.split(',')[1:]
            commodities.append(igr)
        i.close()
        
    for c in commodities:
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
                
    for k,v in coTable.items():
        #print(k,dfs[k[0]],dfs[k[1]])
        d = v*len(commodities)/(dfs[k[0]]*dfs[k[1]]);
        coTable[k] = math.log(d)
    
    """
    t = 1
    for g in coTable:
        print(g,coTable[g])
        t += 1
        if t > 10:
            break
    
    """
    predict_vs_real = {}
    TP = 0 # True positive
    APP = 0 # All predicted positive
    ARP = 0 # All real positive
    for c in range(len(commodities)):
        predrisk = []
        realrisk = []
        miAvrList = {} #{'0':0.0}
        for e in range((int(c/100)+1)*100+50,(int(c/100)+1)*100+100):
            if str(e) in commodities[c]:
                realrisk.append(str(e))
        for x in commodities[c]:
            miSum = 0
            for y in commodities[c]:
                miSum += coTable[(x,y)]
            miAvr = miSum/len(commodities[c])
            miAvrList[x] = miAvr
        miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1))
        for n in range(2):
            predrisk.append(miAvrRank[n][0])
        predict_vs_real[c] = [predrisk,realrisk]
        ARP += len(realrisk)
        for pr in predrisk:
            APP += 1
            if pr in realrisk:
                TP += 1
        #print(c,(predrisk,realrisk))
            
    print('Precision =',str(TP/APP))
    print('Recall =',str(TP/ARP))
    return predict_vs_real
        
def detectRiskByClustering(classified = [], frompath = 'C:/facts/commoditiesN.csv'):
    commodities = []
    if len(classified)>0:
        d = 0
        for i in classified:
            d+=1
            for j in i:
                cla = str(d)
                igr = []
                for f in j:
                    igr.append(str(f))
                commodities.append((cla,igr))
    else:
        i = open(frompath, 'r')
        lines = i.read().split('\n')
        for line in lines:
            cla = line.split(',')[0]
            igr = line.split(',')[1:]
            commodities.append((cla,igr))
        i.close()
            
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
        #print(risks)
        
    predict_vs_real = {}
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
            predict_vs_real[m[0]] = [predrisk,realrisk]
            ARP += len(realrisk)
            for pr in predrisk:
                APP += 1
                if pr in realrisk:
                    TP += 1
            #print(m[0],(predrisk,realrisk))
            
    print('Precision =',str(TP/APP))
    print('Recall =',str(TP/ARP))
    return predict_vs_real

classified = dataGeneration()
detectRiskByClustering(classified)
detectRiskByMutualInfo(classified)
detectRiskByVectorDist(classified)