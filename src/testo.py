file1 = open('C:/facts/longlist.csv', 'r')
file2 = open('C:/facts/shortlist.csv', 'r')
longData = file1.read().split('\n')
shortData = file2.read().split('\n')
file3 = open('C:/facts/longlistNew.csv', 'w')
for i in range(len(longData)):
    if i == 0 :
        file3.write(longData[i]+'\n')
    else :
        if longData[i] in shortData:
            file3.write(longData[i]+',1\n')
        else:
            file3.write(longData[i]+',0\n')
file1.close()
file2.close()
file3.close()