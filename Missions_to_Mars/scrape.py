#import dependencies
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time
import pymongo
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path={'executable_path':ChromeDriverManager().install()}
    return Browser('chrome',**executable_path, headless=False)


# ### NASA Mars News

def scrape():
    browser = init_browser()
    mars_dict ={}
    url='https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)


    # create html object and parse with BeautifulSoup
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    soup


    news_title = soup.find_all('div', class_='content_title')[0].text
    news_body = soup.find_all('div', class_='article_teaser_body')[0].text



    # ### JPL Mars Space Images - Featured Image

    # Mars image scraping
    image_url='https://spaceimages-mars.com/'
    browser.visit(image_url)


    image_html=browser.html
    image_soup=BeautifulSoup(image_html,'html.parser')
    #image_soup


    image_path=image_soup.find_all('img')[1]['src']


    featured_image_url=image_url+image_path
    featured_image_url



    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    tables



    mars_df=tables[0]
    mars_df.columns=['Description','Mars','Earth']
    mars_facts_df=mars_df.drop(index=0)
    mars_facts_df

    mars_html_table = mars_facts_df.to_html()
    mars_html_table

    mars_html_table.replace('\n', '')

    # ### Mars Hemispheres


    hems_url='https://marshemispheres.com/'
    browser.visit(hems_url)


    hems_html=browser.html
    hems_soup=BeautifulSoup(hems_html,'html.parser')
    #hems_soup



    mars_hems = hems_soup.find('div', class_='collapsible results')
    mars_hemispheres = mars_hems.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(hems_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)


    mars_dict = {
            "news_title": news_title,
            "news_p": news_body,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }

    browser.quit()

    return mars_dict
