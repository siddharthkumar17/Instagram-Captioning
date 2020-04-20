from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
from random import choice
import json, re
import pprint as pp
import time

class Scraper:
    def __init__(self, user_name, wait_time=20, max_pages=1):
       
        self.USERNAME = user_name
        
        self.URL = 'https://www.instagram.com/' + self.USERNAME 
        self.WAIT_TIME = wait_time
        self.MAX_PAGES = max_pages

        
    def scrape(self, user_agent = 'Mozilla/5.0'):
        s = requests.Session()
        s.headers['user-agent'] = user_agent
        end_cursor = ''
        images = []

        for x in range(self.MAX_PAGES):

            r    = s.get(self.URL)
            data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)

            j = json.loads(data)
            j = j['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

            end = j['page_info']['has_next_page']
            media = j['edges'] 

            for x in media:
                images.append(x['node']['display_url'])
            
            if not end:
                break
            else:
                time.sleep(self.WAIT_TIME)
        s.close()
        return images

        #pp.pprint(IMAGES)
    def getImagesFromSource(self,images, path = ''):
        output_path=[]
        if path=='':
            for x in range(len(images)):
                output_path .append( 'img/'+self.USERNAME+'_IMG_'+str(x)+'.jpg' )
        else:
            for x in range(len(images)):
                output_path .append( path+str(x)+'.jpg' )
        
       
        for x in range(len(images)):
            urllib.request.urlretrieve(images[x],output_path[x])
            
        return output_path
        