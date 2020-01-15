
# coding: utf-8

#importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
#defining the path to the directory
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

#Visit the NASA Mars News to collect News Title & Paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #soup


    news_title = soup.find('div', class_= "content_title").text
    news_p = soup.find('div', class_ = "rollover_description_inner").text

 

    #Visit the url for JPL featured space image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #soup

    #use splinter to find the mars featured image
    link = soup.find('a', class_='button fancybox')['data-fancybox-href']

    featured_image_url = 'https://www.jpl.nasa.gov' + link
    

    #Mars weather tweets
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #saving the tweet
    try:
        html = browser.html
        #Create BeautifulSoup object; parse with 'html'
        soup = bs(html, 'html.parser')
        mars_weather = soup.find('p', class_='TweetTextSize').text
    except Exception as e:
        print(e)
        mars_weather="tweet not available"
        


    #Mars facts webpage scrape
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)[0].to_html(index=False, header=False)

    #hemispheres

    url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
       
    names = []
    for name in soup.find_all('h3'):
        names.append(name.text[:-9])

           # Find Links to click on, based on hemisphere names list
           # Click the link, find the image url, then go back and repeat
    hemisphere_image_urls = []
    for name in names:
        browser.click_link_by_partial_text(name)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Find image URL
        link = 'https://astrogeology.usgs.gov' + soup.find(class_="wide-image").get('src')
           # and append to list of dicts
        hemisphere_image_urls.append({'title': name, 'img_url': link})

           # Go back to parent site
        browser.back()

       #------------------------------------------------------------------------

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "table": tables,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data
