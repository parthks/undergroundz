from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
import tmdbsimple as tmdb

from selenium import webdriver
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive '
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def rename_file(service, file_id, new_title):
  """Rename a file.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to rename.
    new_title: New title for the file.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    file = {'title': new_title}

    # Rename the file.
    updated_file = service.files().patch(
        fileId=file_id,
        body=file,
        fields='title').execute()

    return updated_file
  except Exception as e:
    print('An error occurred:')
    print(e)
    return None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



f = open('out','r')
allMovies = f.read()
f.close()


tmdb.API_KEY = '78eb1d3ed01f7bbdd8c0d772f3c8a2d1'
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v2', http=http)
solarMovies = 'https://yesmovies.to/movie/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)


allMovies = allMovies.split('\n')
total = len(allMovies)
count = 0
fucked = 0

for moveData in allMovies:
  moveData = moveData.split(' ')
  gkey = moveData[0]
  solarName = moveData[3]
  name = moveData[3].split('-')[:-1]
  name = ' '.join(name)

  
  search = tmdb.Search()
  response = search.movie(query=name)
  results = response['results']

  if len(results) == 1:
      res = results[0]
      d = res['release_date'].split('-')[0]
      title = res['title']
      title = title + ' (' + d + ')'
      print(title)
      rename_file(service, gkey, title)

  else:
      matched = []
      for res in results:
        compare = res['title'].lower()
        if compare == name:
          matched.append(res)

      if len(matched) == 1:
        res = matched[0]
        d = res['release_date'].split('-')[0]
        title = res['title']
        title = title + ' (' + d + ')'
        print(title)
        rename_file(service, gkey, title)

      else:
        link = solarMovies + solarName + '.html'
        driver.get(link)
        time.sleep(1)
        xpathDate = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[3]"
        date = driver.find_element_by_xpath(xpathDate).text.split(': ')[1]
        xpathName = "/html/body[@id='body-search']/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='detail-mod']/h3"
        title = driver.find_element_by_xpath(xpathName).text
        title = title + ' (' + date + ')'
        print(title)
        rename_file(service, gkey, title)

        # print('Fuck!')
        f = open('CHECK', 'a')
        f.write(title+'\n')
        f.close()
        # f.write(gkey+'\n')
        # f.write(solarName+'\n')
        # for res in results:
        #   d = res['release_date'].split('-')[0]
        #   title = res['title']
        #   title = title + ' (' + d + ')'
        #   f.write(title+'\n')

        # f.close()
        # fucked += 1

  count += 1
  print('%d / %d' % (count, total))
  #print('need to manually do %d' % (fucked))






