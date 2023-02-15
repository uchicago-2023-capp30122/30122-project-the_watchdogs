import json
import lxml.html
import requests
from utils import url_to_root, articles_to_list

def scrape_article(url):
    """
    This function takes a URL to a FOX news article and returns a
    dictionary with the title, source (FOX), date published, description, 
    keywords, body of the text.

    Parameters:
        * url:  a URL to a news article on CNN

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the news article page
            * title:        the title of the article
            * source:       the name of the media source (FOX in this case)
            * date:         the publish date
            * description:  the description of the article
            * keywords:     the search keywords for the article
            * text:         the article text itself
    """

    article = {}
    root = url_to_root(url)

    article['source'] = 'FOX'
    article['url'] = url
    article['title'] = root.cssselect("h1")[0].text_content().strip()
    article['date'] = root.cssselect("time")[0].text_content().strip()
    article['description'] = root.xpath("/html/head/meta[7]/@content")[0]
    
    #STILL NEED TO CLEAN
    article['text'] = root.cssselect("div.article-content")[0].text_content().strip()

    return article

def articles_to_json(url_list):
    """
    Given a list of urls, write the respective article dictionaries to a json
    """
    articles = articles_to_list(url_list)
    #CHANGE LOCATION OF THIS WHEN OUT OF TEST PHASE
    with open("test_data/fox_articles.json", "w") as f:
        json.dump(articles, f, indent=1)