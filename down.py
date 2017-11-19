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
from browsermobproxy import Server

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

display = Display(visible=0, size=(700, 700))
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
    local_filename = 'movieFile.mp4'
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian



def new_dl_meth(link): #THIS PART HAS PROBLEMS!!!!
    #path = '/Users/parth/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    #from browsermobproxy import Server
    print('!!NEW METHOD FOR VIP 7!!')
    path = '/root/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(path, options={'port': 9999})
    server.start()
    proxy = server.create_proxy()
    print('Started proxy!')

    profile  = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    browser = webdriver.Firefox(firefox_profile=profile)
    print('Started Firefox!')

    #url = 'https://solarmoviez.ru/movie/sea-oak-season-01-22636/1092432-7/watching.html'

    # xpathDate = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[3]"
    # date = browser.find_element_by_xpath(xpathDate).text.split(': ')[1]
    # xpathName = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='detail-mod']/h3"
    # title = browser.find_element_by_xpath(xpathName).text
    # title = title + ' (' + date + ')'
    # print(title)


    proxy.new_har('HART')
    print_warning('getting link..(again)..')
    browser.get(link)
    print_success('zzzzz')
    time.sleep(5)
    browser.get('https://solarmoviez.ru/movie/star-wars-rebels-the-siege-of-lothal-17597/709439-7/watching.html')
    main_window = browser.current_window_handle
    time.sleep(1)
    el = browser.find_element_by_xpath('//*[@id="sv-7"]/a')
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(el, 5, 5)
    action.click()
    action.perform()
    time.sleep(2)
    #browser.switch_to.alert.accept()
    browser.switch_to_window(main_window)
    browser.find_element_by_xpath('//*[@id="sv-7"]/a').click()
    browser.switch_to_window(main_window)
    browser.current_url
    browser.find_element_by_xpath('//*[@id="sv-14"]/a').click()
    browser.switch_to_window(main_window)
    browser.current_url
    browser.find_element_by_xpath('//*[@id="sv-7"]/a').click()
    browser.current_url


    s = str(proxy.har) # returns a HAR JSON blob
    url = browser.current_url
    start = s.find('https://streaming.lemonstream.me:1443')
    end = s.find(" ",start)
    m3u8 = s[start:end-2]

    key = m3u8.split('/')[3]


    junk_m3u8 = "' -H 'Origin: https://solarmoviez.ru' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,mt;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'Accept: */*' -H 'Referer:"+ url +"' -H 'Connection: keep-alive' --compressed"
    output = subprocess.check_output("curl '"+m3u8+junk_m3u8, shell=True)

    o = str(output)
    start = o.find('seg-',-40)

    end = o.find('-v1-',31350)

    maxNum = o[start:end]
    maxNum = maxNum.split('-')[1]

    gold = o.split('\\n')[-3]
    cutIndex = gold.rfind('/')
    gold = gold[:cutIndex]

    endPart = '/seg-[1-'+maxNum+']-v1-a1.ts'

    goldUrl = 'https://streaming.lemonstream.me:1443/'+key+'/127.0.0.1/'+gold+endPart
    junk_gold = "' -H 'Origin: https://solarmoviez.ru' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,mt;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'Accept: */*' -H 'Referer: "+ url +"' -H 'Connection: keep-alive' --compressed"
    print_success('Starting download')
    server.stop()
    browser.quit()

    subprocess.call("curl -o 'lool_#1.ts' '"+goldUrl+junk_gold, shell=True)

    # name = url.split('/')[-1].split('.')[0] -- NOT THE FULL URL!

    subprocess.call("cat lool_*.ts > movieFile.mp4", shell=True)
    subprocess.call("rm *.ts", shell=True)

    # return 'name.mp4'



def get_download_link(movieLink):
    global driver
    

    try:
        main_window = driver.current_window_handle
        print("getting OPENLOAD link")
        time.sleep(1)
        el = driver.find_element_by_xpath('//*[@id="sv-14"]/a')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 5, 5)
        action.click()
        action.perform()
        time.sleep(2)
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
        # if driver.find_element_by_xpath('//*[@id="player-area"]/div[2]/div[1]/div[1]/span') == 'VIP 7':
        #     dl = 'dl this :P'
        #     print('!!VIP 7!!')
        #     return dl
        el = driver.find_element_by_xpath('//*[@id="sv-6"]/a')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 5, 5)
        action.click()
        action.perform()
        time.sleep(2)
        driver.switch_to_window(main_window)
        time.sleep(2)
        el = driver.find_element_by_xpath('//*[@id="sv-6"]/a')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 5, 5)
        action.click()
        action.perform()
        time.sleep(3)
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


    time.sleep(2)

    xpathDate = '//*[@id="mv-info"]/div/div[2]/div[5]/div[2]/p[3]'
    date = driver.find_element_by_xpath(xpathDate).text.split(': ')[1]
    xpathName = '//*[@id="mv-info"]/div/div[2]/div[2]/h3'
    title = driver.find_element_by_xpath(xpathName).text
    title = title + ' (' + date + ')'
    print(title)

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

    try:
        download_file(dl)
    except Exception as e:
        new_dl_meth(movieLink)
    
    #file = wget.download(dl)
    #urllib.urlretrieve(dl, str(name)+'.mp4', hook)
    file = 'movieFile.mp4'
    print_success("\nfinished downloading!")
    subprocess.call("mkdir '"+str(name)+"'", shell=True)
    subprocess.call("mv "+ file + " '"+str(title)+"'/'"+str(name)+"'.mp4", shell=True)
    logMovie(name)
    
    # print_warning('Sleeping!')
    # time.sleep(60)



def upload_movie(name):
    print("uploading...")
    subprocess.call("cd ..", shell=True)
    time.sleep(0.5)
    # subprocess.call("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r '"+str(name)+"'/", shell=True)
    
    output = subprocess.check_output("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r '"+str(name)+"'/", shell=True)
    print(output)
    code = 'Error 403'
    while code in output:
        print_warning('sleeping for 3 min zzzzz...')
        time.sleep(180)
        output = subprocess.check_output("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r '"+str(name)+"'/", shell=True)

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





