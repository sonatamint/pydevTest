#encoding=utf-8
import os
import jieba
import re
import operator
import math
from sklearn.cluster import KMeans


def segmentOne():
    inglist = open('C:/facts/ingList.txt', 'r', encoding="utf-8")
    alllines = re.sub("\s+|\n", " ", inglist.read())
    for wd in alllines.split(' '):
        jieba.add_word(wd)  
    outfile = open('C:/facts/ingredients.txt', 'w', encoding="utf-8")
    for root, dirs, files in os.walk("C:/facts/label_cut/result/"):
        for f in files:
            infile = open(root+f, 'r', encoding="utf-8")
            instring = infile.read()
            instring = re.sub("\s+", "", instring)
            segs = jieba.cut(instring)
            outstring = " ".join(segs)
            outstring = re.sub("(^| )[^米水盐](?= |$)","", outstring) # filter out one-character-length words saving some special ingredients
            outstring = re.sub("(^| )[0-9a-zA-Z]{2}(?= |$)","", outstring) # filter out two-character-length words composed of non-Chinese
            outstring = re.sub("(^| )(配料|过敏|信息|制造|本品|生产|设备|同时|含有|产品)(?= |$)","", outstring) # stop word list
            outfile.write(f+" "+outstring+"\n")
            infile.close()
    outfile.close()   

segmentOne() 

vocab = []
filenames = []
inp = open('C:/facts/ingredients.txt', 'r', encoding="utf-8") 
ot1 = open('C:/facts/indexedCommd.csv', 'w') 
ot2 = open('C:/facts/dictionary.csv', 'w', encoding="utf-8") 
classes = [] 
commodities = [] 
comdcsv = ''
dictcsv = ''
lines = inp.read().strip('\n').split('\n')
for l in range(len(lines)):
    line = lines[l]
    line = re.sub("\s+"," ", line)
    cd = line.split(' ')[0]
    filenames.append(cd)
    igrs = line.split(' ')[1:]
    for i in range(len(igrs)):
        if igrs[i] in vocab:
            igrs[i] = vocab.index(igrs[i])
            if i==0:
                comdcsv += '0,'+str(igrs[i]) # all unclassified commodities go to class 0
            else:
                comdcsv += ','+str(igrs[i])
        else:
            vocab.append(igrs[i])
            igrs[i] = vocab.index(igrs[i])
            if i==0:
                comdcsv += '0,'+str(igrs[i])
            else:
                comdcsv += ','+str(igrs[i])
            if l==0 and i==0:
                dictcsv += str(igrs[i])+','+vocab[igrs[i]]
            else:
                dictcsv += '\n'+str(igrs[i])+','+vocab[igrs[i]]
    
    commodities.append(igrs)
    if l<len(lines)-1:
        comdcsv += '\n'

classes.append(commodities) # in case of no class labels but IDs of commodities, all the commodities are treated as of a single class
ot1.write(comdcsv)
ot2.write(dictcsv)
ot1.close()
ot2.close()

def detectRiskByMutualInfo(classified = [], frompath = 'C:/facts/indexedCommd.csv', vocab = vocab, classNum = 1, realriskpath = 'C:/facts/risks.txt'):
    commodities = [] # all commodities are arranged in the same order as in the input text file
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
    '''
    t = 1
    for g in coTable:
        print(g,coTable[g])
        t += 1
        if t > 10:
            break
    '''
    predict_vs_real = {}
    if os.path.isfile(realriskpath):
        supervis = open(realriskpath, 'r')
        lines = supervis.read().split('\n')
        TP = 0 # True positive
        APP = 0 # All predicted positive
        ARP = 0 # All real positive
        for c in range(len(commodities)):
            predrisk = []
            miAvrList = {} #{'0':0.0}
            realrisk = lines[c].split(' ')[1:]
            for k in range(len(realrisk)):
                realrisk[k] = vocab.index(realrisk[k])
            for x in commodities[c]:
                miSum = 0
                for y in commodities[c]:
                    miSum += coTable[(x,y)]
                miAvr = miSum/len(commodities[c])
                miAvrList[x] = miAvr
            miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1)) # ingredients ranked in ascending order 
            # according to their average mutual information with other ingredients from the same commodity
            '''
            for mi in miAvrRank:
                if mi[1] < 2.5: # threshold
                    predrisk.append(int(mi[0]))
            '''        
            predrisk.append(int(miAvrRank[0][0]))
            predrisk.append(int(miAvrRank[1][0]))
            # choose the smallest 2 mi as risk ingredients
            predict_vs_real[c] = [predrisk,realrisk]
            ARP += len(realrisk)
            for pr in predrisk:
                APP += 1
                if pr in realrisk:
                    TP += 1
            print(c,(predrisk,realrisk))
        print('Precision =',str(TP/APP))
        print('Recall =',str(TP/ARP))
    else:
        for c in range(len(commodities)):
            predrisk = []
            realrisk = []
            miAvrList = {} #{'0':0.0}
            for x in commodities[c]:
                miSum = 0
                for y in commodities[c]:
                    miSum += coTable[(x,y)]
                miAvr = miSum/len(commodities[c])
                miAvrList[x] = miAvr
            miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1))
            '''
            for mi in miAvrRank:
                if mi[1] < 2.5: # threshold
                    predrisk.append(int(mi[0]))
            '''
            if len(miAvrRank)>1:
                #predrisk.append(int(miAvrRank[0][0]))
                predrisk.append(vocab[int(miAvrRank[0][0])])
                #predrisk.append(int(miAvrRank[1][0]))
                predrisk.append(vocab[int(miAvrRank[1][0])])
            elif len(miAvrRank)>0:
                #predrisk.append(int(miAvrRank[0][0]))
                predrisk.append(vocab[int(miAvrRank[0][0])])
            predict_vs_real[c] = [predrisk,realrisk]
            print(filenames[c],(predrisk,realrisk))
                
    return predict_vs_real

def detectRiskByClustering(classified = [], frompath = 'C:/facts/indexedCommd.csv', vocab = vocab, classNum = 1, realriskpath = 'C:/facts/risks.txt'):
    commodities = [] # in case of a single class, the commodities are arranged in the same order as in the input text file
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
            
    tfidf = [] # has the same order as commodities
    for c in commodities:
        voc = [0 for n in range(len(vocab))]
        for i in c[1]:
            voc[int(i)] = 1
        tfidf.append(voc)
        
    km = KMeans(n_clusters=classNum)
    clusters = km.fit_predict(tfidf)
    types = set(clusters) #class labels
    classes = []
    for c in types:
        clustered = []
        for d in range(len(commodities)):
            if clusters[d] == c: # class label for each commodity
                    clustered.append((d,tfidf[d]))
        classes.append(clustered)
    
    risky = []
    for cluster in classes: # find risky ingredients for each class
        frequency = dict([(n,0) for n in range(len(vocab))])
        for m in cluster: # m = (d,tfidf[d])
            for x in range(len(vocab)):
                frequency[x] = frequency[x] + m[1][x]
        risks = [] 
        for k,v in frequency.items():
            if v>1 and v<3 :
                risks.append(k)
        '''
        sorted_f = sorted(frequency.items(), key=operator.itemgetter(1))
        thred = len(cluster) # ingredients with frequency = 0 and the len(cluster) most rarely appeared ingredients with frequency > 0
        b = 0
        for g in sorted_f:
            if g[1] == 0:
                pass #risks.append(g[0])
            elif b < thred:
                risks.append(g[0])
                b += 1
        '''
        risky.append(risks)
        #print('risks for this class:',risks)
    
    predict_vs_real = {}
    if os.path.isfile(realriskpath):
        supervis = open(realriskpath, 'r')
        lines = supervis.read().split('\n')
        TP = 0 # True positive
        APP = 0 # All predicted positive
        ARP = 0 # All real positive
        for l in range(len(classes)):
            cluster = classes[l]
            risks = risky[l]
            for m in cluster: # m = (d,tfidf[d])
                predrisk = []
                realrisk = lines[m[0]].split(' ')[1:]
                for k in range(len(realrisk)):
                    realrisk[k] = vocab.index(realrisk[k])
                for r in risks:
                    if m[1][r] > 0:
                        predrisk.append(r)
                predict_vs_real[m[0]] = [predrisk,realrisk]
                ARP += len(realrisk)
                for pr in predrisk:
                    APP += 1
                    if pr in realrisk:
                        TP += 1
                print(m[0],(predrisk,realrisk))  
        print('Precision =',str(TP/APP))
        print('Recall =',str(TP/ARP))
    else:
        for l in range(len(classes)):
            cluster = classes[l]
            risks = risky[l]
            for m in cluster: # m = (d,tfidf[d])
                predrisk = []
                realrisk = []
                for r in risks:
                    if m[1][r] > 0:
                        predrisk.append(vocab[r])
                predict_vs_real[m[0]] = [predrisk,realrisk]
                print(filenames[m[0]],(predrisk,realrisk))
                
    return predict_vs_real
    

detectRiskByClustering(classified=classes,realriskpath="")
#detectRiskByMutualInfo(classified=classes,realriskpath="")















