from subprocess import check_output
import time

def write_to_file(arr):
    f = open('empties', 'w')
    f.write(str(arr))
    f.close()


f = open('out', 'r')
l = f.read()
f.close()
data = l.split('\n')

count = 1
empty = 0
total = len(data)

empties = []
for x in data:
    key = x.split(' ')[0]
    Done = False
    while(not Done):
        try:
            print(key)
            out = check_output('gdrive list --query "' + "'" + key + "'" +' in parents" --bytes --no-header', shell=True)
            Done = True
        except Exception as e:
            print('zzzzzz...')
            time.sleep(10)
        
    
    #if str(out) != "b''":
    try:
        size = str(out).split(' ')[9]
        print(size)
    except Exception as e:
        print('EMPTY!')
        size = 0
        
    if int(size) < 50:
        empties.append(key)
        empty += 1

    print('done with '+str(count)+' of '+str(total))
    print('empty = '+str(empty))
    print('ratio = '+str((empty / (count*1.0))*100))
    count += 1

    if (count % 500) == 0:
        write_to_file(empties)


write_to_file(empties)
