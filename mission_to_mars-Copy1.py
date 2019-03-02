#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

response=requests.get('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
soup = BeautifulSoup(response.text, 'html.parser')


# In[2]:


latest_headline = soup.find('div', class_="content_title").text.strip()
teaser = soup.find('div', class_="rollover_description_inner").text.strip()
teaser


# In[15]:


#executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', headless=False)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
html=browser.html
soup = BeautifulSoup(html, 'html.parser')

image=soup.find("footer").find('a')['data-fancybox-href']
featured_image_url="https://www.jpl.nasa.gov/" + image
featured_image_url


# In[4]:


twitter_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter_url)
html=browser.html
soup = BeautifulSoup(html, 'html.parser')

latest_tweet = soup.find('p', class_="tweet-text").text.strip()
latest_tweet


# In[5]:


url = 'http://space-facts.com/mars/'
tables = pd.read_html(url)
df = tables[0]


# In[6]:


html_table = df.to_html()
html_table


# In[7]:


html_table.replace('\n', '')


# In[8]:


urls = [
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
]


# In[19]:


info = {}
for address in urls:
    browser.visit(address)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img=soup.find("div", id="wide-image").find("img", class_="wide-image")['src']
    img_url="https://astrogeology.usgs.gov/" + img
    title=soup.find("title").text.split()[0]
    info.update({title:img_url})
info    


# In[ ]:




