import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape ():
    browser=init_browser ()
    return {
        'mars_news': mars_news(browser),
        'mars_featured_image': mars_image (browser),
        'mars_facts':mars_facts (),
        'mars_hemispheres': mars_hemispheres (browser)
    }

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    news_titles = {}    
    url='https://mars.nasa.gov/news/'
    time.sleep(2)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_= 'content_title').text.strip()
    news_p = soup.find_all('p')
    news_titles['news_title']= news_title
    news_titles['news_paragraph']=news_p

    return news_titles

def mars_image(browser):
    full_image = {}
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit (url)
    image_full=browser.find_by_id('full_image')
    image_full.click()
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    img_url = soup.find('img', class_ = 'main_image')['src']
    featured_img_url = "https://www.jpl.nasa.gov" + img_url
    full_image ['featured_img_url'] = featured_img_url
    return full_image 

def mars_facts():
 
    facts_df =pd.read_html('https://space-facts.com/mars/')[1]
    facts_df.columns=["Description","Values"]
    facts_df=facts_df.to_html()

    return facts_df
  
def mars_hemispheres(browser):
    mars_news = {}
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit (url)
    html_hemispheres = browser.html
    soup = bs(html_hemispheres , 'html.parser')

    hemisphere_image_urls = []
    products = soup.find ('div', class_='result-list')
    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=BeautifulSoup(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    hemisphere_image_urls
    mars_news ['hemisphere_image_urls']= hemisphere_image_urls

    return  hemisphere_image_urls
