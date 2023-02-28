import json
import lxml.html
import requests
from utils import url_to_root
from bs4 import BeautifulSoup

def crawl_cnn(base_url):
    response = requests.get(base_url).text
    response = json.loads(response)
    results = response['result']

    articles = []

    for result in results:
        a = {}
        a['url'] = result['url']
        a['source'] = 'CNN'
        a['title'] = result['headline']
        a['date'] = result['lastModifiedDate']
        a['text'] = result['body']
        articles.append(a)
    
    return articles



#when creating the crawler make sure the url does NOT include 'live-news'
def scrape_cnn_result(url):
    """
    This function takes a URL to a CNN news result and returns a
    dictionary with the title, source (CNN), date published, description, 
    keywords, body of the text.

    Parameters:
        * url:  a URL to a news result on CNN

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the news result page
            * title:        the title of the result
            * source:       the name of the media source (CNN in this case)
            * date:         the publish date
            * description:  the description of the result
            * keywords:     the search keywords for the result
            * text:         the result text itself
    """

    result = {}
    root = url_to_root(url)

    result['url'] = url
    result['title'] = root.cssselect("h1")[0].text_content().strip()
    result['source'] = 'CNN'
    result['description'] = root.xpath("/html/head/meta[6]/@content")[0]
    
    #change keywords to a list 
    keywords_string = root.xpath("/html/head/meta[21]/@content")[0]
    result['keywords'] = keywords_string.split(", ")
    
    #clean and add date
    date = root.cssselect("div.timestamp")[0].text_content()
    result['date'] = date.replace('\n', '').replace('  ', '').replace('Updated', '')

    #clean and add body text
    text = root.cssselect("div.result__content")[0].text_content().strip()
    text = text.replace('\n', '').replace('  ', '')
    result['text'] = text
    
    #for mitch mcconnel result ... check to see if this in others
    result['text'] = result['text'][13:]

    return result

def results_to_json(base_url):
    """
    Given a base url, write the respective result dictionaries to a json
    """

    articles = crawl_cnn(base_url)

    with open("data/cnn_results.json", "w") as f:
        json.dump(articles, f, indent=1)

