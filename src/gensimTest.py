#encoding=utf-8
from gensim.models import word2vec

o = open('C:/facts/commodities-noID.csv', 'r')    
content = o.read()
modified = content.replace(',',' ')
o.close() # print(modified)
i = open('C:/facts/text8test', 'w')
i.write(modified)
i.close()
sentences=word2vec.Text8Corpus('C:/facts/text8test')
model=word2vec.Word2Vec(sentences,min_count=1,size=50)
print(100,model['100'])

"""
a=model.similarity("967", "978")
b=model.most_similar("967", topn=3)
c=model.most_similar(positive=['333', '555'], negative=['888'], topn=3)
print(a)
print(b)
print(c)
"""

d = open('C:/facts/commodities-noID.csv', 'r')
predict_vs_real = []
TP = 0 # True positive
APP = 0 # All predicted positive
ARP = 0 # All real positive
lines = d.read().split('\n')
for l in range(len(lines)):
    igr = lines[l].split(',')
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
    print(l, (predrisk,realrisk))
    
print('Precision =',str(TP/APP))
print('Recall =',str(TP/ARP))