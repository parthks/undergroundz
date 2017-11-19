import json

import wget
import requests
import subprocess
from threading import Thread
import threading
import time


doneMovies = []
f = open('gotten', 'r')
for line in f:
    doneMovies.append(line)
f.close()

f = open('REAL-DL-LINKS', 'r')
link_dict = json.load(f)
f.close()



def download_file(key):
    global link_dict
    print('downloading '+str(key))
    url = link_dict[key][0]
    local_filename = 'movieFile.mp4'
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    filee = 'movieFile.mp4'
    name = key
    print(name)
    subprocess.call('mkdir "'+str(name)+'"', shell=True)
    subprocess.call('mv '+ filee + ' "'+str(name)+'"/"'+str(name)+'".mp4', shell=True)

    output = subprocess.check_output('gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r "'+str(name)+'"/', shell=True)
    print(output)
    code = 'Error 403'
    while code in output:
        print_warning('sleeping for 5 min zzzzz...')
        time.sleep(300)
        output = subprocess.check_output("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r '"+str(name)+"'/", shell=True)

    print('done uploading... "'+str(name)+'"/')
    subprocess.call('rm -r "'+str(name)+'"/', shell=True)
    print('done deleting "'+str(name)+'"/')




done = 0
blank = 0
count = 0
for key in link_dict:
    count += 1
    if link_dict[key] == []:
        blank += 1
        continue

    if key in doneMovies:
        print('done!')
        done += 1
        continue

    print(link_dict[key][0])
    #file = wget.download(link_dict[key][0])

    while threading.active_count()-1 > 5:
        time.sleep(5)

    thread = Thread(target=download_file, args=[key])
    thread.start()

    print('COUNT = '+str(count))
    print('BLANK = '+str(blank))
    print('DONE = '+str(done))





