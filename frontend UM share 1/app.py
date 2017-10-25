import subprocess
import json

from flask import render_template
from flask import request


from flask import Flask


# 
# subprocess.call("cd ..", shell=True)
# fileID = '0B5SLYItizrrvRnowSG5RT0Q1RTQ'
# email = 'parths.97@gmail.com'


f = open('MovieGoogleIDs.txt', 'r')
allMoviezDict = json.load(f)
f.close()


sharedFiles = []


#fileID = allMoviezDict[name]

def logShare(MovId):
    f = open('sharedFiles.txt', 'a')
    f.write(MovId + '\n')
    f.close()


def logData(name, email):
    f = open('MovieLog.txt', 'a')
    f.write(email +' - '+ name +'\n')
    f.close()




def share(yoid, email):
    logShare(yoid)
    subprocess.call("gdrive share --type user --email "+email+" "+yoid, shell=True)
    #subprocess.call("gdrive share --type anyone "+yoid, shell=True)
    

def revoke(fileID, email):
    output = subprocess.check_output("gdrive share list "+fileID, shell=True)
    permissID = clean_output_getID(output, email)
    subprocess.call("gdrive share revoke "+fileID+" "+permissID, shell=True)



def clean_output_getID(inp, email):
    #out = {}

    inp = inp.split('\n')
    inp.pop(0)

    for arr in inp:
      arr = arr.split(' ')
      arr = filter(None, arr)
      if len(arr) < 2:
        continue
      #print arr
      ID = arr[0]
      Email = arr[3].lower()
      #out[Email] = ID
      if Email == email:
          #print Email
          return ID



def searchForMovie(q):
    q = q.replace(' ','-')
    return [key for key in allMoviezDict if q in key] #should make it an array for here only




app = Flask(__name__)

@app.route('/')
def hello():

    return render_template('index.html')



@app.route('/res', methods=['POST'])
def results():
    if request.method == 'POST':
        query = request.form['movie']
        email = request.form['email']

        arr = searchForMovie(query)

    return render_template('results.html', allMoviez=arr, user_email=email)




@app.route('/get', methods=['POST'])
def get():
    if request.method == 'POST':
        movie = request.form['movie']
        email = request.form['email']

        fileID = 'Please log in...!'

        if email != 'blank':
            fileID = allMoviezDict[movie]
            share(fileID, email)
        
        logData(movie, email)

    return render_template('moviez.html', movID=fileID, userEmail=email)



if __name__ == "__main__":
    # here is starting of the development HTTP server
    app.run()



