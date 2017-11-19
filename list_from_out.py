''' 
first run:
gdrive list --query "'0B5SLYItizrrvbk51R3JXb0Y5Zkk' in parents" --name-width 0 --no-header -m 10000 > out
'''
f = open('out','r')
d = f.read()
f.close()
l = d.split('\n')
#del l[0]
f = open('gotten','w')

for i in l:
    try:
        m = i.split('        ')[1] + '\n'
    except Exception as e:
        print(i)
        m='0'
   
    f.write(m)

f.close()