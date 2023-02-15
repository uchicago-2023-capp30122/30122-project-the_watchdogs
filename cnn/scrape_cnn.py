import json
import lxml.html
import requests
from utils import url_to_root

#when creating the crawler make sure the url does NOT include 'live-news'
def scrape_cnn_article(url):
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
    article['description'] = root.xpath("/html/head/meta[6]/@content")[0]
    
    #change keywords to a list 
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

def articles_to_json(url_list):
    """
    Given a list of urls, write the respective article dictionaries to a json
    """
    articles = []

    for url in url_list:
        articles.append(scrape_cnn_article(url))

    #CHANGE LOCATION OF THIS WHEN OUT OF TEST PHASE
    with open("test_data/cnn_articles.json", "w") as f:
        json.dump(articles, f, indent=1)









