#encoding=utf-8
import os
import jieba
import re

inglist = open('C:/facts/ingList.txt', 'r', encoding="utf-8")
alllines = re.sub("\s+|\r\n", " ", inglist.read())
for wd in alllines.split(' '):
    if len(wd)==1:
        print(wd)
'''
    jieba.add_word(wd)       


outfile = open('C:/facts/ingredients.txt', 'w')
for root, dirs, files in os.walk("C:/facts/label_cut/result/"):
    for f in files:
        infile = open(root+f, 'r', encoding="utf-8")
        instring = infile.read()
        instring = re.sub("\W+", "", instring)
        segs = jieba.cut(instring)
        outstring = " ".join(segs)
        outstring = re.sub(" [_丿] | [_丿]$"," ", outstring)
        outstring = re.sub(" \d{1,2} | \d{1,2}$| [a-zA-Z]{1,2} | [a-zA-Z]{1,2}$"," ", outstring)
        outfile.write(f+" "+outstring+"\n")
        infile.close()
outfile.close()   

'''