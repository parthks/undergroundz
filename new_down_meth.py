from browsermobproxy import Server
from selenium import webdriver
import subprocess
import time

path = '/Users/parth/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy'
server = Server(path)
server.start()
proxy = server.create_proxy()

profile  = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
browser = webdriver.Firefox(firefox_profile=profile)

url = 'https://solarmoviez.ru/movie/sea-oak-season-01-22636/1092432-7/watching.html'


# xpathDate = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[3]"
# date = browser.find_element_by_xpath(xpathDate).text.split(': ')[1]
# xpathName = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='detail-mod']/h3"
# title = browser.find_element_by_xpath(xpathName).text
# title = title + ' (' + date + ')'
# print(title)


proxy.new_har('HART')
browser.get(url)
time.sleep(5)

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
subprocess.call("curl -o 'lool_#1.ts' '"+goldUrl+junk_gold, shell=True)

# name = url.split('/')[-1].split('.')[0] -- NOT THE FULL URL!

subprocess.call("cat lool_*.ts > movieFile.mp4", shell=True)
subprocess.call("rm *.ts", shell=True)

# return 'name.mp4'

server.stop()
browser.quit()
