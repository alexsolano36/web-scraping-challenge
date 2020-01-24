from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape():
#Replace the path with actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    #mars.nasa.gov/news/
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Scrape page into Soup
    html = browser.html
    nasa_soup = bs(html, 'html.parser')

    #Returned results
    summary = nasa_soup.find('div', class_="rollover_description_inner").text
    title = nasa_soup.find('div', class_="content_title").text
        
    print(f"Title: {title}")
    print(f"Summary: {summary}")

    #Visit URL for JPL Featured Space Image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)

    html = browser.html
    space_soup = bs(html, 'html.parser')

    #using splinter to find mars featured image
    image = space_soup.find('a', class_='fancybox') ['data-fancybox-href']
    image_url = 'https://www.jpl.nasa.gov' + image
    print(image_url)

    #Mars weather tweets
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)

    try:
        html = browser.html
        weather_soup = bs(html, 'html.parser')

        #save tweet
        mars_weather = weather_soup.find('p', class_ = "TweetTextSize").text
        print(mars_weather)
    except Exception as e:
        print(e)
        mars_weather = "Latest Mars Weather Tweet not Available. Try again later."

    #Mars facts scrape
    facts_url = 'https://space-facts.com/mars/'
    mars_info = pd.read_html(facts_url)[0].to_html(index=False, header=False)
    mars_info

    #hemispheres photo scraping
    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
        
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = bs(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_= "wide-image")["src"]
        
        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url
        print(img_dict["img_url"])
        
        hemisphere_image_urls.append(img_dict)
        
    mars_data = {
        "title": title,
        "summary": summary,
        "image_url": image_url,
        "mars_weather": mars_weather,
        "mars_info": mars_info,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data
