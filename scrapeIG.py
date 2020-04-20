from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
from random import choice
import json, re
import pprint as pp
import time

USERNAME = 'sidkumar17'
IMAGES = []
URL = 'https://www.instagram.com/' + USERNAME 
WAIT_TIME = 20
MAX_PAGES = 1

s = requests.Session()
s.headers['user-agent'] = 'Mozilla/5.0'

end_cursor = ''



for x in range(MAX_PAGES):

    r    = s.get(URL)
    data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)

    j = json.loads(data)
    j = j['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

    end = j['page_info']['has_next_page']
    media = j['edges'] 

    for x in media:
        IMAGES.append(x['node']['display_url'])
    
    if not end:
        break
    else:
        time.sleep(WAIT_TIME)

#pp.pprint(IMAGES)
x=0
for img in IMAGES:
    urllib.request.urlretrieve(img, 'img/'+USERNAME+'_IMG_'+str(x)+'.jpg')
    x+=1

s.close()