import json
import lxml.html
import requests
import re
from utils import url_to_root

def get_page_url(base_url, page_number):
    """
    Given the fox api base url and a search result page number, get the url

    Input:
        base_url (str): the base url
        page_number (int): the page number
    
    Returns:
        (str): the desired url
    """
    if page_number > 10:
        return KeyError('Page number cannot be greater than 10')
    else:
        new_url = base_url.replace(f'&start=1&callback=__jp1', f'&start={page_number - 1}1&callback=__jp{page_number}')
        return new_url

def api_json_to_dict(api_url, page_number):
    """
    Given an api.foxnews.com url, create a dictionary of the page information

    Input:
        api_url (str): the url 
        page_number (int): page number in search results where 0 is the base_url
    
    Returns:
        (dict): a dictionary of the page info
    """
    response = requests.get(api_url).text
    response = response.replace(f'// API callback\n__jp{page_number}(', '')[:-2]

    return json.loads(response)

def gather_urls(base_url):
    """
    Given a a url from a fox api, gather all the article urls from that page and 
    all subsequent pages

    Input:
        base_url(str): the base url for the fox api (page 1)
    Returns:
        (list): a list of urls of fox api's site
    """
    url_list = []
    url = base_url
    
    for i in range(10):
        page_number = i + 1
        page_info = api_json_to_dict(url, page_number)
        num_items = len(page_info['items'])
        for item in range(num_items):
            url = page_info['items'][item]['link']
            #ensure the url is to a news article and is not live
            if ('/category/' not in url) and ('/live-news/' not in url):  
                url_list.append(url)
        url = get_page_url(base_url, page_number + 1)
    
    return url_list

def scrape_fox_article(url):
    """
    This function takes a URL to a FOX news article and returns a
    dictionary with the title, source (FOX), date published, description, 
    and body of the text.

    Input:
        result (dict): a dicitionary of a FOX article 

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the article page
            * title:        the title/headline of the article
            * source:       the name of the media source (FOX in this case)
            * date:         the most recently modified date
            * description:  the description of the article
            * text:         the article body text
    """

    article = {}
    root = url_to_root(url)

    article['url'] = url
    article['source'] = 'FOX'
    article['title'] = root.cssselect("h1")[0].text_content().strip()
    article['description'] = root.xpath("/html/head/meta[7]/@content")[0]
    article['date'] = root.cssselect("time")[0].text_content().strip()
    
    #clean and add body text
    text = ''
    for p in root.cssselect("p"):
        if (p.getchildren() == []) and (p.get('class') == None):
            text += str(p.text_content())
    
    article['text'] = text.replace("\xa0", "").replace("\"", "\'")
    
    return article

#base_url = 'https://api.foxnews.com/search/web?q=January%206%20insurrection%20capitol+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section&siteSearch=foxnews.com&siteSearchFilter=i&start=1&callback=__jp1'
def crawl_fox(base_url):
    """
    Given the base url of a fox api, write the respective article dictionaries 
    to a json

    Input:
        base_url(str): the base url for the fox api (page 1)
    """
    articles = []
    url_list = gather_urls(base_url)

    for url in url_list:
        articles.append(scrape_fox_article(url))

    with open("data/fox_articles.json", "w") as f:
        json.dump(articles, f, indent=1)
