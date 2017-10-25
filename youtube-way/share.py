# Content ID flags vids even when PRIVATE! - SHIRRTTT

import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#from pyvirtualdisplay import Display


import time
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import urllib
import requests
import math
import subprocess


# Open https://www.youtube.com/edit?video_id=d2d3_MmlE8s based on vid ID
# Click with class yt-uix-button yt-uix-button-size-default yt-uix-button-default metadata-share-button
# Enter in textarea - email to share
# Click by name notify_via_email button
# Click the share button

f = open('password', 'r')
gm_password = f.read()
f.close()

link = 'https://youtu.be/5YHwqa79Jok'
emailToShare = 'parths.97@gmail.com'

# display = Display(visible=0, size=(800, 600))
# display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.get(link)
time.sleep(0.5)
email = driver.find_element_by_id('identifierId')

email.send_keys('bogusemailforme01')
time.sleep(0.5)
driver.find_element_by_class_name('RveJvd').click()

p = driver.find_elements_by_class_name('whsOnd')[0]
p.send_keys(gm_password)
time.sleep(0.5)

edit = driver.find_element_by_class_name('metadata-share-button')
edit.click()

p = driver.find_element_by_class_name('metadata-share-contacts')
p.send_keys(emailToShare)

p = driver.find_element_by_class_name('notify-via-email')
p.click()
time.sleep(0.5)

p = driver.find_element_by_class_name('sharing-dialog-ok')
p.click()
time.start(0.5)

p = driver.find_elements_by_class_name('save-changes-button')
p[1].click()

