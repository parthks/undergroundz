from subprocess import call
import time

f = open('empties', 'r')
data = f.read()
f.close()

l = data.split(', ')
l[0] = l[0][1:]
l[len(l)-1] = l[len(l)-1][:-1]

count = 0

for key_id in l:
    key_id = key_id.replace("'",'')
    Done = False
    call('gdrive delete -r '+key_id, shell=True)
    
    print(count, len(l))
    count += 1
    # while(not Done):
    #     try:
    #         call('gdrive delete -r '+key_id, shell=True)
    #         Done = True
    #     except Exception as e:
    #         print('Failed to delete')
    #         time.sleep(5)

