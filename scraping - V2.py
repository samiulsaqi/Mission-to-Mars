#import Dependencies
from splinter import Browser as Br
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import requests


def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Br('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping and store results in dictionary
    data ={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": features_image(browser),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser),
        "facts": mars_facts()
    }

    #close browser
    browser.quit()

    return data

def mars_news(browser):
    #set URL and visit first website
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
   
    #optional delay for loading page
    browser.is_element_present_by_css("ul_item_list li.slide", wait_time=1)

    #set BS element and search within for scraping
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # find paragraph text
        news_p = slide_elem.find("div", class_= "article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    #return values
    return news_title, news_p

def features_image(browser):
    
    ### FEATURED IMAGE SCRAPPING

    #VISIT URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    base_url = "https://www.jpl.nasa.gov"
    html = browser.html
    list_soup = soup(html, 'html.parser')
    link_list = list_soup.find_all('div', {'class': 'SearchResultCard'})[0]
    img_soup = link_list.select_one('a').get('href')
    full_url = base_url + img_soup
    browser.visit(full_url)
    
    html = browser.html
    a_soup = soup(html, 'html.parser')
    
    
    try:
        # Find the relative image url
        link = a_soup.find('a', {'class': 'BaseButton text-contrast-none w-full mb-5 -primary -compact inline-block'}).get('href')
    
    except AttributeError:
        return None
    
        
    return link

def mars_facts():
    try:
        #read html table into pandas dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['Description','Mars']
    df.set_index('Description',inplace=True)
    df

    #export scraped table to html format
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    #Parse the resulting html with soup
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

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())