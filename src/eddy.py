import re

f = open('D:/tracks_AVISO_DT2014_daily_web.ascii', 'r')
inpu=f.read()
lines=inpu.split('\n')
print(len(lines))

map=[(x,y) for x in range(0,650) for y in range(-80,80)]
table=dict([(x,0) for x in map])
#print(table)

regex = re.compile('\s+')

i = 0
for line in lines:
    if i%6 == 1:
        life = int(float(regex.split(lines[i-1].strip())[1]))
        if life>112:
            longs = regex.split(line.strip())
            latis = regex.split(lines[i+1].strip())
            num = regex.split(lines[i-1].strip())[0]
            print(num,life)
            added = set()
            for t in range(len(longs)):
                key = (int(float(longs[t])), int(float(latis[t])))
                if key not in added:
                    table[key] = table[key]+1
                    added.add(key)
    i = i+1

for k,v in table.items():
    if k[0]>=360:
        table[(k[0]-360,k[1])] = table[(k[0]-360,k[1])] + table[k] 
        

o = open('D:/result.csv', 'w')
o.write('x,y,n\n')
for k,v in table.items():
    if (v>0) and (k[0]<360):
        o.write(str(k[0])+','+str(k[1])+','+str(v)+'\n')
        #o.write(str(k)+','+str(v)+'\n')
        
