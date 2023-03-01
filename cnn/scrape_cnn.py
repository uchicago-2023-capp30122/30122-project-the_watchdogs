import json
import lxml.html
import requests
from utils import url_to_root
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime

def scrape_cnn_result(result):
    """
    Given a result json from the CNN api, scrape the article and create a dictionary

    Input:
        result (dict): a dicitionary of a CNN article 

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the article page
            * title:        the title/headline of the article
            * source:       the name of the media source (CNN in this case)
            * date:         the most recently modified date
            * description:  the description of the article
            * text:         the article body text
    """

    article = {}
    #get the info from the json
    article['url'] = result['url']
    article['source'] = 'CNN'
    article['title'] = result['headline']
    article['description'] = result['description']

    #change date format to match FOX format
    article['date'] = result['lastModifiedDate'].strftime("%B %d, %Y %I:%M%p %Z")

    #clean and add body text
    b = bytes(result['body'], encoding = "utf-8")
    article['text'] = str(b, encoding = "ascii", errors = "ignore")

    return article

def get_description(url):
    """
    Given a url get the description attribute from its html

    Input:
        url (str): the url
    Returns:
        (str): description of the article
    """
    root = url_to_root(url)
    description = root.xpath("/html/head/meta[6]/@content")[0]
    description = description.replace("\"", "\'").strip()

    return description

def check_date(date):
    """
    Check that a date is in desired range for research (Jan 6 2021 - Jan 7 2023)

    Input:
        date (datetime format): article date from last modified
    
    Returns:
        (bool): True if date is in range
                False otherwise
    """
    if date.year in range(2021, 2023):
        if (date.year == 2023):
            if (date.month) > 1:
                return True
            elif (date.day <= 7):
                return True
            else:
                return False
        if (date.year == 2021):
            if (date.month) > 1:
                return True
            elif (date.day >= 6):
                return True
            else:
                return False
    else:
        return False

def scraping_conditions(result):
    """
    Check attributes of the article to ensure it is scrapable

    Input:
        result (dict): a dicitionary of a CNN article 

    Returns:
        (bool): True if meets scraping conditions
                False otherwise
    """
    date = result['lastModifiedDate']
    media_type = result['type']
    description = result['description']
    headline = result['headline']
    
    if ((media_type == 'article') and (description != 'unsafe-url') and 
        (headline[:16] != '5 things to know') and (check_date(date))):
        return True
    else:
        return False

def scrape_page(url):
    """
    Given CNN's api of search results, scrape all articles from search results,
    creating a dictionary for each article, and returning a list of all articles

    Input: 
        url (str): a url of CNN api search results (search.api.cnn.com)
    
    Returns:
        (list): a list of articles (dictionaries)
    """
    response = requests.get(url).text
    response = json.loads(response)
    results = response['result']

    articles = []
    for result in results:
        #add article info to result that is not in the API
        result['lastModifiedDate'] = dateutil.parser.isoparse(result['lastModifiedDate'])
        result['description'] = get_description(result['url'])
        
        if scraping_conditions(result):
            articles.append(scrape_cnn_result(result))
    
    return articles

def crawl_cnn(url):
    """
    Given a url of CNN api search results, scrape all articles and write to a json

    Input: 
        url (str): a url of CNN api search results (search.api.cnn.com)
    """
    response = requests.get(url).text
    response = json.loads(response)
    meta = response['meta']
    

    #calculate max pages to crawl
    articles_per_page = meta['total']
    total_articles = meta['of']
    pages = total_articles / articles_per_page
    max_pages = total_articles // articles_per_page
    if pages % 1 != 0:
        max_pages += 1

    articles = []
    for page_num in range(1, max_pages + 1):
        #generate new url
        url_parts = url.split('&')
        start = int(url_parts[2][5:])
        new_start = ['from=' + str(start + articles_per_page)]
        new_page = ['page=' + str(page_num + 1)]
        url_lst = url_parts[:2] + new_start + new_page + url_parts[-2:]
        url = "&".join(url_lst)
        #get articles from the next page and add to the list
        articles += scrape_page(url)

    with open("data/cnn_articles.json", "w") as f:
        json.dump(articles, f, indent=1)
