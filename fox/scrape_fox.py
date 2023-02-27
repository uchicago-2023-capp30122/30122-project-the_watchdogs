import json
import lxml.html
import requests
from utils import url_to_root

#base_url = 'https://api.foxnews.com/search/web?q=January%206%20insurrection%20capitol+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section&siteSearch=foxnews.com&siteSearchFilter=i&start=1&callback=__jp1'
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
    """
    url_list = []
    url = base_url
    
    for i in range(10):
        page_number = i + 1
        #print(page_number)
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
    keywords, body of the text.

    Parameters:
        * url:  a URL to a news article on FOX

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
    
    #Still need to remove article links and backslashes
    text = root.cssselect("div.article-content")[0].text_content().strip()
    article['text'] = text.replace(u'\xa0', u' ').replace("  "," ").replace("\'", "'")

    return article

def crawl_fox(base_url):
    """
    Given a list of urls, write the respective article dictionaries to a json
    """
    articles = []
    url_list = gather_urls(base_url)

    for url in url_list:
        articles.append(scrape_fox_article(url))

    with open("data/fox_articles.json", "w") as f:
        json.dump(articles, f, indent=1)





