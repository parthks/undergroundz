import subprocess


f = open('sharedFiles.txt', 'r')
allMoviez = f.read()
allMoviez = allMoviez.split('\n')
print allMoviez
print len(allMoviez)


def clean_output_getID(inp):
    inp = inp.split('\n')
    inp.pop(0)
    ids = []

    for arr in inp:
      arr = arr.split(' ')
      arr = filter(None, arr)
      if len(arr) < 2:
        continue
      #print arr
      ID = arr[0]
      Email = arr[3].lower()

      if Email != 'parthks@umich.edu':
          ids.append(ID)
      
    return ids




for fileID in allMoviez:
    if fileID == "":
        continue
    output = subprocess.check_output("gdrive share list "+fileID, shell=True)
    #print output

    permissIDs = clean_output_getID(output)

    for permissID in permissIDs:
        subprocess.call("gdrive share revoke "+fileID+" "+permissID, shell=True)


f.close()


f = open('sharedFiles.txt', 'w')
f.close()