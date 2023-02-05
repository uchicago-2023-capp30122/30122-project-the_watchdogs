import sys
import json
import lxml.html
import requests
from utils import url_to_root

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
    #get title, remove the ' | CNN Politics' at the end
    article['title'] = root.cssselect("title")[0].text_content()[:-15]
    article['source'] = 'CNN'
    article['date'] = 'xx'
    article['description'] = 'xx'
    article['keywords'] = 'xx'
    article['text'] = 'xx'

    return article









