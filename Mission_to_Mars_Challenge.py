#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import Splinter and BeautifulSoup
from splinter import Browser as Br
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Br('chrome', **executable_path, headless=False)

url = 'https://mars.nasa.gov/news'
browser.visit(url)

#optional delay for loading page
browser.is_element_present_by_css("ul_item_list li.slide", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# find paragraph text
news_p = slide_elem.find("div", class_= "article_teaser_body").get_text()
news_p

### FEATURED IMAGE SCRAPPING

#VISIT URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)

#find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

#find the more info button and click that
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description','values']
df.set_index('description',inplace=True)

df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
response = requests.get(url)
# Parse the resulting html with soup
hem_soup = soup(response.text, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
base_url = 'https://astrogeology.usgs.gov'

# 3. Write code to retrieve the image urls and titles for each hemisphere.

hem_links = [base_url + a['href'] for a in hem_soup.find_all('a', {'class': 'product-item'})]
hem_links


#initiate for loop to get links to image and title
for link in hem_links:
    
    #find link to 'sample' jpg image and title under h2
    hem_page = soup(requests.get(link).text, 'html.parser')
    
    img_url = hem_page.find('div', {'class': 'downloads'}).find('a', text='Sample')['href']

    title = hem_page.find('h2', {'class':'title'}).text
    
    #append link and title to list as a dictionary item
    hemisphere_image_urls.append(dict([('img_url', img_url),('title', title)]))

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()