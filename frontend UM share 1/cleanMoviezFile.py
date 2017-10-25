import subprocess
import json


f = open('1-578-moviez', 'r')
allMoviez = f.read()
f.close()

MovieIDAndName = {}

allMoviez = allMoviez.split('\n')
allMoviez.pop(0)

for arr in allMoviez:
  arr = arr.split(' ')
  #print arr
  arr = filter(None, arr)
  #print arr
  if len(arr) < 2:
    continue
  ID = arr[0]
  Name = arr[1] 
  MovieIDAndName[ID] = Name
  MovieIDAndName[Name] = ID


f = open('moviez', 'r')
allMoviez = f.read()
f.close()

allMoviez = allMoviez.split('\n')
allMoviez.pop(0)

for arr in allMoviez:
  arr = arr.split(' ')
  arr = filter(None, arr)
  if len(arr) < 2:
    continue
  ID = arr[0]
  Name = arr[1] 
  MovieIDAndName[ID] = Name
  MovieIDAndName[Name] = ID





print(len(MovieIDAndName))

y = open('MovieGoogleIDs.txt', 'w')
json.dump(MovieIDAndName, y)
y.close()










