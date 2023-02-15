import sys
import json
import lxml.html
from lxml import etree
import requests
from utils import url_to_root

url="https://www.cnn.com/2022/02/09/politics/mitch-mcconnell-violent-insurrection/index.html"

#when creating the crawler make sure the url does NOT include 'live-news'

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
    article['title'] = root.cssselect("h1")[0].text_content().strip()
    article['source'] = 'CNN'
    #check to see if this xpath is universal
    article['description'] = root.xpath("/html/head/meta[6]/@content")[0]
    
    #change keywords to a list 
    ##check to see if this xpath is universal
    keywords_string = root.xpath("/html/head/meta[21]/@content")[0]
    article['keywords'] = keywords_string.split(", ")
    
    #clean and add date
    date = root.cssselect("div.timestamp")[0].text_content()
    article['date'] = date.replace('\n', '').replace('  ', '').replace('Updated', '')

    #clean and add body text
    text = root.cssselect("div.article__content")[0].text_content().strip()
    text = text.replace('\n', '').replace('  ', '')
    article['text'] = text
    #for mitch mcconnel article ... check to see if this in others
    article['text'] = article['text'][13:]


    return article

def articles_to_list(url_list):
    """
    Given a list of urls of articles, create a list of thier article dictionaries

    Input: url_list (list): of urls 
    
    Returns: list of dictionaries
    """

    articles = []

    for url in url_list:
        articles.append(scrape_article(url))

    return articles

    #output is a list of articles

def articles_to_json(articles):
    """
    """

    with open("test_data/cnn_articles.json", "w") as f:
        json.dump(articles, f, indent=1)









