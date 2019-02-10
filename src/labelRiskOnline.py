#encoding=utf-8
import os
import jieba
import re
import operator
import math
from sklearn.cluster import KMeans


vocab = []
commodities = [] #[(filename,int[igrs])]
classes = [] # [[indexes of commodities in class i]]
risky = [] # [int[classrisks]]
dfs = {} #{'0':0}
coTable = {} #{('0','0'):0.0}

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

#segmentOne() 

def initial(datapath='C:/facts/ingredients.txt', riskpath='C:/facts/risks.txt', classNum=1, requireTest=False): # if class is known, run with classNum=1 in each class folder
    inp = open(datapath, 'r', encoding='utf-8') 
    lines = inp.read().strip('\n').split('\n')
    tfidf = [] # has the same order and length as commodities
    for l in range(len(lines)):
        line = lines[l].strip()
        line = re.sub('\s+',' ', line)
        cd = line.split(' ')[0]
        igrs = line.split(' ')[1:]
        for i in range(len(igrs)):
            if igrs[i] in vocab:
                igrs[i] = vocab.index(igrs[i])
            else:
                vocab.append(igrs[i])
                igrs[i] = vocab.index(igrs[i])
        commodities.append((cd,igrs))   
    inp.close()
    for c in commodities:
        for x in c[1]:
            if x in dfs.keys():
                dfs[x] += 1
            else:
                dfs[x] = 1
            for y in c[1]:
                if (x,y) in coTable.keys():
                    coTable[(x,y)] += 1.0
                else:
                    coTable[(x,y)] = 1.0
                
    for k,v in coTable.items():
        d = v*len(commodities)/(dfs[k[0]]*dfs[k[1]]);
        coTable[k] = math.log(d)
    if os.path.isfile(riskpath):
        risklist = [] #[(filename,int[risks])]
        inpt = open(riskpath, 'r', encoding='utf-8')
        content = inpt.read().strip('\n')
        lines = content.split('\n')
        for l in range(len(lines)):
            line = lines[l].strip()
            line = re.sub('\s+',' ', line)
            cd = line.split(' ')[0]
            risks = line.split(' ')[1:]
            for i in range(len(risks)):
                if risks[i] in vocab:
                    risks[i] = vocab.index(risks[i])
                else:
                    vocab.append(risks[i])
                    risks[i] = vocab.index(risks[i])
            risklist.append((cd,risks))
        outstr = ''
        for c in commodities:
            voc = [0 for n in range(len(vocab))]
            for i in c[1]:
                voc[i] = 1
            tfidf.append(voc)
        km = KMeans(n_clusters=classNum)
        clusters = km.fit_predict(tfidf)
        types = set(clusters) #class labels
        for c in types:
            cluster = []
            for d in range(len(commodities)):
                if clusters[d] == c: # class label for each commodity
                        cluster.append(d)
            classes.append(cluster)
        for cluster in classes: # find risky ingredients for each class
            risks = set()
            for m in cluster:
                for n in risklist:
                    if n[0]==commodities[m][0]:
                        risks.update(n[1])
            risks = list(risks) 
            risky.append(risks)
            #print('Risk in class '+str(cluster)+' is: '+str([vocab[j] for j in risks]))
        inpt.close()
        if requireTest:
            testrst = ''
            TP = 0 # True positive
            APP = 0 # All predicted positive
            ARP = 0 # All real positive
            for l in range(len(classes)):
                cluster = classes[l]
                realclassrisks = risky[l]
                predclassrisks = []
                frequency = dict([(n,0) for n in range(len(vocab))])
                for m in cluster:
                    for x in range(len(vocab)):
                        frequency[x] = frequency[x] + tfidf[m][x] # after adding new commodities the length of vocab will change
                for k,v in frequency.items():
                    if v>1 and v<3 :
                        predclassrisks.append(k)
                for m in cluster:
                    testrst += commodities[m][0]+' predicted:'
                    predrisk = []
                    realrisk = []
                    miAvrList = {} #{'0':0.0}
                    for x in commodities[m][1]:
                        miSum = 0
                        for y in commodities[m][1]:
                            miSum += coTable[(x,y)]
                        miAvr = miSum/len(commodities[m][1])
                        miAvrList[x] = miAvr
                    miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1)) # ingredients ranked in ascending order 
                    # according to their average mutual information with other ingredients from the same commodity
                    n = 0
                    for e in miAvrRank: # choose the n=2 ingredients in class risk with the smallest mi as commodity risk
                        if e[0] in predclassrisks:
                            predrisk.append(e[0])
                            testrst += ' '+vocab[e[0]]
                            n += 1
                            if n > 1:
                                break
                    '''
                    for r in predclassrisks:
                        if tfidf[m][r] > 0:
                            predrisk.append(r)
                            testrst += ' '+vocab[r]
                    '''
                    testrst += ' real:'
                    for r in realclassrisks:
                        if tfidf[m][r] > 0:
                            realrisk.append(r)
                            testrst += ' '+vocab[r]
                    testrst += '\n'
                    ARP += len(realrisk)
                    for pr in predrisk:
                        APP += 1
                        if pr in realrisk:
                            TP += 1
            testrst += 'Precision = '+str(TP/(APP+1))+'\n'
            testrst += 'Recall = '+str(TP/(ARP+1))
            return testrst    
        else:
            return content
    else:
        outstr = ''
        for c in commodities:
            voc = [0 for n in range(len(vocab))]
            for i in c[1]:
                voc[i] = 1
            tfidf.append(voc)
        km = KMeans(n_clusters=classNum)
        clusters = km.fit_predict(tfidf)
        types = set(clusters) #class labels
        for c in types:
            cluster = []
            for d in range(len(commodities)):
                if clusters[d] == c: # class label for each commodity
                        cluster.append(d)
            classes.append(cluster)
        for cluster in classes: # find risky ingredients for each class
            frequency = dict([(n,0) for n in range(len(vocab))])
            for m in cluster:
                for x in range(len(vocab)):
                    frequency[x] = frequency[x] + tfidf[m][x]
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
            for m in cluster:
                outstr += commodities[m][0]
                miAvrList = {} #{'0':0.0}
                for x in commodities[m][1]:
                    miSum = 0
                    for y in commodities[m][1]:
                        miSum += coTable[(x,y)]
                    miAvr = miSum/len(commodities[m][1])
                    miAvrList[x] = miAvr
                miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1)) # ingredients ranked in ascending order 
                # according to their average mutual information with other ingredients from the same commodity
                n = 0
                for e in miAvrRank: # choose the 2 ingredients in class risk with the smallest mi as commodity risk
                    if e[0] in risks:
                        outstr += ' '+vocab[e[0]]
                        n += 1
                        if n > 1:
                            break
                outstr += '\n'
                
        outp = open(riskpath, 'w', encoding='utf-8')
        outp.write(outstr.strip('\n'))
        outp.close()
        return outstr.strip('\n')
    

print(initial(classNum=1,requireTest=True))

def onebyone(datapath='C:/facts/ingredients.txt', riskpath='C:/facts/risks.txt', strpath='', kofknn=9):
    if os.path.isfile(strpath):
        outfile = open(datapath, 'a', encoding="utf-8")
        infile = open(strpath, 'r', encoding="utf-8")
        instring = infile.read()
        instring = re.sub("\s+", "", instring)
        segs = jieba.cut(instring)
        outstring = " ".join(segs)
        outstring = re.sub("(^| )[^米水盐](?= |$)","", outstring) # filter out one-character-length words saving some special ingredients
        outstring = re.sub("(^| )[0-9a-zA-Z]{2}(?= |$)","", outstring) # filter out two-character-length words composed of non-Chinese
        outstring = re.sub("(^| )(配料|过敏|信息|制造|本品|生产|设备|同时|含有|产品)(?= |$)","", outstring) # stop word list
        outstring = strpath[strpath.rfind('/')+1:]+" "+outstring
        outfile.write('\n'+outstring)
        infile.close()
        outfile.close() 
        line = re.sub('\s+',' ', outstring.strip())
        cd = line.split(' ')[0]
        igrs = line.split(' ')[1:]
        for i in range(len(igrs)):
            if igrs[i] in vocab:
                igrs[i] = vocab.index(igrs[i])
            else:
                vocab.append(igrs[i])
                igrs[i] = vocab.index(igrs[i])
        jsim = {} # has the same order as commodities
        for c in range(len(commodities)): # Jaccard similarity = A∩B/A∪B
            AnB = 0
            AUB = len(commodities[c][1]) + len(igrs)
            for i in igrs:
                if i in commodities[c][1]:
                    AnB += 1
                    AUB -= 1
            jsim[c] = AnB/(AUB+1)
            print(commodities[c][0]+' jsim is '+str(jsim[c])) ###
        simRank = sorted(jsim.items(), key=operator.itemgetter(1), reverse = True) # similarity ranked in descending order 
        k = 0
        clscount = [0 for n in range(len(classes))]
        for it in simRank:
            for l in range(len(classes)):
                if it[0] in classes[l]:
                    clscount[l] += 1
            k += 1
            if k > kofknn:
                break
        belongs = 0
        for l in range(len(classes)):
            if clscount[l] > clscount[belongs]:
                belongs = l
        print(classes[belongs]) ###
        print('Risk in this class is: '+str([vocab[j] for j in risky[belongs]])) ###
        outstr = cd
        miAvrList = {} #{'0':0.0}
        for x in igrs:
            miSum = 0
            for y in igrs:
                if (x,y) in coTable.keys():
                    miSum += coTable[(x,y)]
            miAvr = miSum/len(igrs)
            miAvrList[x] = miAvr
        miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1)) # ingredients ranked in ascending order 
        # according to their average mutual information with other ingredients from the same commodity
        n = 0
        for e in miAvrRank: # choose the 2 ingredients in class risk with the smallest mi as commodity risk
            if e[0] in risky[belongs]:
                outstr += ' '+vocab[e[0]]
                n += 1
                if n > 1:
                    break
        '''
        for i in igrs:
            if i in risky[belongs]:
                outstr += ' '+vocab[i]
        '''       
        print('Detected risk is: '+outstr)
        a = input('Real risk is (separate with a single space): ')
        if len(a.strip())==0: # no input means the predicted risk is right
            outr = open(riskpath, 'a', encoding='utf-8')
            outr.write('\n'+outstr)
            outr.close()
            commodities.append((cd,igrs))
            classes[belongs].append(len(commodities)-1)
        else: # parse the input text and store it as risk
            outr = open(riskpath, 'a', encoding='utf-8')
            outr.write('\n'+cd+' '+a)
            outr.close()
            outstr = cd+' '+a
            commodities.append((cd,igrs))
            classes[belongs].append(len(commodities)-1)
            for g in a.split(' '):
                if g in vocab:
                    x = vocab.index(g)
                    if x not in risky[belongs]:
                        risky[belongs].append(x)
                else:
                    vocab.append(g)
                    x = vocab.index(g)
                    risky[belongs].append(x)
        return outstr
    else:
        return 'Please input the full path of an ingredient file.'


inglist = open('C:/facts/ingList.txt', 'r', encoding="utf-8")
alllines = re.sub("\s+|\n", " ", inglist.read())
for wd in alllines.split(' '):
    jieba.add_word(wd)
while True:
    a = input('Input file:')
    print(onebyone(strpath=a,kofknn=9))
















