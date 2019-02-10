import codecs

i = codecs.open('C:/facts/Processed', 'r', 'utf-8')
lines = i.read(2000).split('\n')
for l in range(100):
    print(lines[l])