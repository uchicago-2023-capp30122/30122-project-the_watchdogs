import sys
import json
import lxml.html
from lxml import etree
import requests
from utils import url_to_root
from bs4 import BeautifulSoup

#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
html="""
<p>hello <b>there</b></p>
"""
soup = BeautifulSoup(html, 'html.parser')
p = soup.find('p')
print(p.string)
print(p.text)

url="https://www.cnn.com/2022/02/09/politics/mitch-mcconnell-violent-insurrection/index.html"

def scrape_article(url):
    """
    This function takes a URL to a CNN news article and returns a
    dictionary with the title, source (CNN), date published, description, 
    keywords, body of the text.

    Parameters:
        * url:  a URL to a news article on CNN

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the news article page
            * title:        the title of the article
            * source:       the name of the media source (CNN in this case)
            * date:         the publish date
            * description:  the description of the article
            * keywords:     the search keywords for the article
            * text:         the article text itself
    """

    article = {}
    root = url_to_root(url)

    article['url'] = url
    article['title'] = root.cssselect("h1.headline__text")[0].text_content().strip()
    article['text'] = root.cssselect("div.article__content")[0].text_content().strip("\n")
    article['source'] = 'CNN'
    article['date'] = root.cssselect("div.timestamp")[0].text_content()
    article['description'] = root.xpath("/html/head/meta[6]")
    article['keywords'] = 'xx'

    return article









