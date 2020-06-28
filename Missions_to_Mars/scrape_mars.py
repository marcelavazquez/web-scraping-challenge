
# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import re


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    print("hola")
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'lxml'
    html = browser.html
    soup = bs(html, "lxml")

    # Retrieve the parent divs for the article
    result = soup.find('div', class_='list_text')

    # scrape the article header 
    news_title = result.find('div', class_='content_title').text

    # scrape the article subheader
    news_p = result.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)

    ### JPL Mars Space Images - Featured Image

    # URL where image is locates
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)

    # Click FULL IMAGE button
    browser.click_link_by_id("full_image")
    time.sleep(2)

    # Click More Info button
    # browser.links.find_by_partial_text("more info")
    browser.click_link_by_partial_text("more info")

    # Create BeautifulSoup object; parse with 'lxml'
    html_img = browser.html
    soup = bs(html_img, "lxml")

    # Scrape for featured image and save url
    featured_url = soup.find('img', class_='main_image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + featured_url
    featured_image_url

    ### Mars Weather

    #visiting the URL for the Mars Weather Twitter Account with splinter
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)

    #creating HTML object and parsing
    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')

    browser.is_element_present_by_xpath("/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div/div[2]/div/div/div/div/article/div/div[2]", wait_time = 1)

    soup = bs(browser.html, "html.parser")

    mars_weather = soup.find(text = re.compile("InSight"))

    print(mars_weather)     

    ### Mars Facts

    # URL of Mars facts
    facts_url = 'https://space-facts.com/mars/'

    # We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
    tables = pd.read_html(facts_url)
    myTable = tables[0]
    myTable.columns = ['Parameter','Value']
    myTable
    myTable.to_html("table_mars.html")

    ### Mars Hemispheres

    # URL of USGS Astrology
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    #creating HTML object and parsing
    html_hem = browser.html
    soup = bs(html_hem, 'html.parser')

    # Retrieve the parent divs for all images
    results = soup.find_all("div", class_="item")

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main URL for the USGS Astrology
    main_url = 'https://astrogeology.usgs.gov'

    # loop over results to get image data
    for result in results:
        # scrape the title
        title = result.find('h3').text
        # scrape the full img url
        half_full_img = result.find('a', class_='itemLink product-item')['href']
        # go to the link with the full image
        browser.visit(main_url + half_full_img)
        #creating HTML object and parsing
        html_individual = browser.html
        soup = bs(html_individual, 'html.parser')
        # Retrieve full image source 
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        # Append to a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    browser.quit()
    hemisphere_image_urls

    #
    ### Store Data
    #

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": myTable,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()


    # Return results
    return mars_data

