f = open('out','r')
d = f.read()
f.close()
l = d.split('\n')
del l[0]
f = open('gotten','a+')

for i in l:
    try:
        m = i.split(' ')[3] + '\n'
    except Exception as e:
        print(i)
        m='0'
   
    f.write(m)

f.close()