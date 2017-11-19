from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By # By.XPATH ; By.ID ; By.CSS_SELECTOR

import time

import urllib
import requests
import wget
import math
import subprocess
import json

import random
from threading import Thread
import threading


#driver.get('https://www.fmovies.io/kind/movies.html?page=1')


def write_to_file(name, some_string):
    f = open(name, 'w')
    f.write(some_string)
    f.close()

def write_links_to_file():
    allLinks = []
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    try:
        f = open('fmovies_LINKS','r')
        allLinks = json.load(f)
        f.close()
    except Exception as e:
        f.close()


    pages = 560 # Do this page - last page dont have 25 links!
    max_pages = 561

    while (pages < max_pages):
        gotcha = False

        while(not gotcha):
            try:
                driver.get('https://www.fmovies.io/kind/movies.html?page='+str(pages))
        
                time.sleep(2)
                for num in range(1,25):
                    x = '/html/body/div/article[1]/ul[2]/li['+str(num)+']/figure/a'
                    link = driver.find_element_by_xpath(x).get_attribute('href')
                    allLinks.append(link)
                    #driver.get(link)
                gotcha = True
            except Exception as e:
                print('zzzzz')
                time.sleep(120)
                
            

        if pages % 10 == 0:
            write_to_file('fmovies_LINKS', json.dumps(allLinks))

        # if pages % 100:
        #     time.sleep(30)
        print('num of links got = '+str(len(allLinks)))
        time.sleep(random.randrange(10,42))

        pages += 1

    driver.quit()
    write_to_file('fmovies_LINKS', json.dumps(allLinks))


# write_links_to_file()
# exit()

def dl_fmovies_LINKS():
    f = open('fmovies_LINKS','r')
    allLinks = json.load(f)
    f.close()

    name_link_dict = {}

    f = open('REAL-DL-LINKS','r')
    name_link_dict = json.load(f)
    f.close()

    
    count = len(name_link_dict)-1
    max_count = len(allLinks)

    # count = start
    # max_count = end

    print(count)


    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    numGotten = 0

    while count < max_count:
        link = allLinks[count]

        gotcha = False

        while(not gotcha):
            driver.get(link)
            #This. is. not. how. u. du. eh.
            # try:
            #     element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
            # finally:
            #     pass
            # wait until an element appears - USE THIS METHOD, waits can be v long!
            # driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/a')
            print('I can see the elements')
            try:
                dl_link = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/a').get_attribute('href')
                title_xpath = '/html/body/div[1]/div[4]/div[1]/div[5]/div[2]/div[1]'
                title = driver.find_element_by_xpath(title_xpath).text
                date_xpath = '/html/body/div[1]/div[4]/div[1]/div[5]/div[2]/div[6]/div[2]'
                date = driver.find_element_by_xpath(date_xpath).text.split(': ')[1]
                gotcha = True

            except Exception as e:
                print(e)
                print('Trying again..zzzzz90')
                time.sleep(90)
        

        title = title + ' (' + str(date) + ')'


        gotcha = False

        while(not gotcha):
            driver.get(dl_link)
            #This. is. not. how. u. du. eh.
            # try:
            #     element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
            # finally:
            #     pass
            # print('I can see the elements')
            #79,80,28 - check those :P
            all_a_tags = driver.find_elements_by_css_selector('a')
            if len(all_a_tags) == 0:
                print("zzzzz30")
                time.sleep(30)
                continue
            links = []
            og_links = []
            gotOne = False
            for a_tag in all_a_tags:
                if (a_tag.text.find('1080P') != -1):
                    og_links.append(a_tag.get_attribute('href'))
                    gotOne = True
                else:
                    if (a_tag.text.find('720P') != -1):
                        link = a_tag.get_attribute('href')
                        links.append(link)
                        gotOne = True
            links = og_links + links
            gotcha = True

           


        name_link_dict[title] = links
        print(title)
        #print(links)
        if count % 10 == 0:
            write_to_file('REAL-DL-LINKS', json.dumps(name_link_dict))

        # if count % 100:
        #     time.sleep(30)

        if gotOne:
            numGotten += 1
        #print('got '+str(numGotten))
        print('%d / %d' % (count, max_count))
        count += 1
        # snor = random.randrange(10,20)
        # print(snor)
        time.sleep(3)

    write_to_file('REAL-DL-LINKS', json.dumps(name_link_dict))



def dl_one_link(index):
    
    global name_link_dict, allLinks, num_of_threads


    print('getting link for '+str(index))

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    link = allLinks[index]

    gotcha = False

    while(not gotcha):
        driver.get(link)
        try:
            dl_link = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/a').get_attribute('href')
            title_xpath = '/html/body/div[1]/div[4]/div[1]/div[5]/div[2]/div[1]'
            title = driver.find_element_by_xpath(title_xpath).text
            date_xpath = '/html/body/div[1]/div[4]/div[1]/div[5]/div[2]/div[6]/div[2]'
            date = driver.find_element_by_xpath(date_xpath).text.split(': ')[1]
            gotcha = True

        except Exception as e:
            #print(e)
            print('Trying again..zzzzz90')
            time.sleep(90)
    

    title = title + ' (' + str(date) + ')'


    gotcha = False

    while(not gotcha):
        driver.get(dl_link)

        all_a_tags = driver.find_elements_by_css_selector('a')
        if len(all_a_tags) == 0:
            print("zzzzz30")
            time.sleep(30)
            continue
        links = []
        og_links = []
        gotOne = False
        for a_tag in all_a_tags:
            if (a_tag.text.find('1080P') != -1):
                og_links.append(a_tag.get_attribute('href'))
                gotOne = True
            else:
                if (a_tag.text.find('720P') != -1):
                    link = a_tag.get_attribute('href')
                    links.append(link)
                    gotOne = True
        links = og_links + links
        gotcha = True

       

    name_link_dict[title] = links
    print(title)
    driver.quit()
    num_of_threads -= 1
    return
    #print(links)




f = open('REAL-DL-LINKS','r')
name_link_dict = json.load(f)
f.close()

f = open('fmovies_LINKS','r')
allLinks = json.load(f)
f.close()

count = len(name_link_dict)

num_of_threads = 0




while count < len(allLinks):

    if threading.active_count()-1 > 10:
        continue

    thread = Thread(target=dl_one_link, args=[count])
    thread.start()
    #num_of_threads += 1
    print('NUM OF THREADS = '+str(threading.active_count()-1))
    print('count = '+str(count))
    count+=1
    if count % 10 == 0:
        write_to_file('REAL-DL-LINKS', json.dumps(name_link_dict))
        print('WRITEN TO FILE! to file! to file')

    if count == len(allLinks)-10:
        f = open('fmovies_LINKS','r')
        allLinks = json.load(f)
        f.close()

    time.sleep(3)
    


#write_links_to_file()

#dl_fmovies_LINKS()
