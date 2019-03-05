
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

#def init_browser():
    #return Browser("chrome", headless=False)

def scrape_info():
    #scrape mars news
    response=requests.get('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
    soup = BeautifulSoup(response.text, 'html.parser')
    latest_headline = soup.find('div', class_="content_title").text.strip()
    teaser = soup.find('div', class_="rollover_description_inner").text.strip()

    #scrape freatured image
    browser = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image=soup.find("footer").find('a')['data-fancybox-href']
    featured_image_url="https://www.jpl.nasa.gov" + image
    
    #scrape twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    latest_tweet = soup.find('p', class_="tweet-text").text.strip()

    #scrape facts
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description','Values']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')

    #scrape hemisphere images
    urls = [
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    ]
    info = []
    for address in urls:
        browser.visit(address)
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img=soup.find("div", id="wide-image").find("img", class_="wide-image")['src']
        img_url="https://astrogeology.usgs.gov" + img
        title=soup.find("title").text.split()[0]
        dicts={'title':title, 'img_url':img_url}
        info.append(dicts)

    mars_data = {
        "latest_headline": latest_headline,
        "teaser": teaser,
        "featured_image": featured_image_url,
        "latest_tweet" : latest_tweet,
        "data_table": html_table,
        "hemi_images": info
    }
        
    browser.quit()
        
    return mars_data
