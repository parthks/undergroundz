#download movies from allMovieLinks.txt
#basically from an array of movie links
#essentially the exact same as down.py
#allMovieLinks.txt is descending IMBD ratings
#11 machies - downloading 12000+ movies, ~1000 movies each droplet

TILL = 1000
START = 0

import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pyvirtualdisplay import Display

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import requests
import wget
import math
import subprocess


"""
Prints message in red.
"""
def print_error(message):
    print '\033[31m{}\033[0m'.format(str(message))

"""
Prints message in yellow.
"""
def print_warning(message):
    print '\033[33m{}\033[0m'.format(str(message))

"""
Prints message in green.
"""
def print_success(message):
    print '\033[32m{}\033[0m'.format(str(message))


currentPercent = -1
def hook(arg1, arg2, arg3):
    global currentPercent
    #print(arg1, arg2, arg3)
    if arg1 != 0:
        numBlocks = arg3 / float(arg2)
        percent = math.floor((float(arg1) / numBlocks) * 100)
        #print(percent)
        if percent > currentPercent:
            currentPercent = percent
            print_success(str(currentPercent)+"%", end='')



# url = 'https://ph2dol.oloadcdn.net/dl/l/HixliSej0z1-8vrM/yDTIgWU2U3c/Forest.Warrior.1996.720p.BluRay.x264.YIFY.mp4?mime=true'
# urllib.urlretrieve(url, 'name.mp4', hook)

# raw_input("hi STOP!")

#url = 'https://openload.co/embed/yDTIgWU2U3c/Forest.Warrior.1996.720p.BluRay.x264.YIFY.mp4'


f = open('allMovieLinks.txt', 'r')
allMovieLinks = json.load(f)
f.close()

counter = START
doneMovies = []
errorMovies = []

display = Display(visible=0, size=(800, 600))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

#driver.get(url)
driver = 0

def logMovie(name):
    f = open('gotten.txt', 'a')
    f.write(name + '\n')
    f.close()

def logError(name):
    f = open('errorDown.txt', 'a')
    f.write(name + '\n')
    f.close()


def download_file(url):
    local_filename = 'movieFile'
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_download_link(movieLink):
    global driver
    

    try:
        main_window = driver.current_window_handle
        print("getting OPENLOAD link")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail']/div[@class='md-top']/div[@id='player-area']/div[@class='pa-server']/div[@class='pas-header']/div[@class='pash-choose']/div[@class='btn-group']/ul[@id='servers-list']/li[@id='sv-14']/a").click()
        time.sleep(1)
        driver.switch_to_window(main_window)
        time.sleep(1)
        driver.switch_to.frame("iframe-embed")
        time.sleep(1)
        driver.find_element_by_id("videooverlay").click()
        time.sleep(1)
        driver.find_element_by_class_name("vjs-big-play-button").click()
        time.sleep(1)
        
        try:
            dl = driver.find_element_by_id("mgvideo_html5_api").get_attribute("src")
        except Exception as e:
            dl = driver.find_element_by_id("olvideo_html5_api").get_attribute("src")

        return dl;
        
    except Exception as e:
        print("getting VIP 6 link")
        driver.get(movieLink)
        time.sleep(1)
        main_window = driver.current_window_handle
        driver.find_element_by_xpath("/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail']/div[@class='md-top']/div[@id='player-area']/div[@class='pa-server']/div[@class='pas-header']/div[@class='pash-choose']/div[@class='btn-group']/ul[@id='servers-list']/li[@id='sv-6']/a").click();
        time.sleep(1)
        driver.switch_to_window(main_window)
        time.sleep(1)
        dl = driver.find_element_by_class_name("jw-video").get_attribute("src")
        return dl;

        


def AmBlocked():
    global driver
    try:
        driver.find_element_by_id("recaptcha_submit")
        sys.exit('IP BLOCKED HAHAHAHA! TIME FOR NEW DROPLET!')

    except Exception as e:
        print_success('You live to download another movie ;)')
        return


def get_movie(name, link):
    global driver
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
    print_success("Started Chrome!! YAYY")
    print_success(link)

    driver.get(link)

    AmBlocked()


    time.sleep(0.5)

    movieLink = driver.find_element_by_class_name('bwac-btn').get_attribute("href")
    driver.get(movieLink)

    time.sleep(0.5)

    dl = get_download_link(movieLink)
    
    print_warning("starting download!")
    driver.quit()

    time.sleep(0.5)
    print('\n')
    print_warning(dl);
    print('\n')
    file = download_file(dl)
    #file = wget.download(dl)
    #urllib.urlretrieve(dl, str(name)+'.mp4', hook)

    print_success("\nfinished downloading!")
    subprocess.call("mkdir '"+str(name)+"'", shell=True)
    subprocess.call("mv "+ file + " '"+str(name)+"'/'"+str(name)+"'.mp4", shell=True)
    logMovie(name)
    
    # print_warning('Sleeping!')
    # time.sleep(60)



def upload_movie(name):
    print("uploading...")
    subprocess.call("cd ..", shell=True)
    time.sleep(0.5)
    subprocess.call("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r '"+str(name)+"'/", shell=True)
    print("done uploading... '"+str(name)+"'/")
    subprocess.call("rm -r '"+str(name)+"'/", shell=True)
    print("done deleting '"+str(name)+"'/")
   


f = open('gotten', 'r')
for line in f:
    doneMovies.append(line)
f.close()

f = open('gotten.txt', 'r')
for line in f:
    doneMovies.append(line)
f.close()

f = open('errorDown.txt', 'r')
for line in f:
    errorMovies.append(line)
f.close()


#print doneMovies


while TILL >= counter:
    
    link = allMovieLinks[counter]
    name = link.split('/')[-1].split('.')[0]
    print name
    print_warning("current counter at "+str(counter))
    counter += 1

    if (name+'\n') in doneMovies:
        print_success("already done, yay!")
        continue

    if (name+'\n') in errorMovies:
        print_warning("already errored, yay!")
        continue

    try:
        get_movie(name,link)
        upload_movie(name)
    except Exception as e:
        print_error("some error :P")
        #subprocess.call("rm *.tmp", shell=True)
        print_warning(e)
        logError(name)
        try:
            driver.quit()
        except Exception as i:
            pass
        continue
 

print_success("OMG ALL DONE HAHAHAH!!!")





