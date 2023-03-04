
##the following code was written by lindsey

import sys
import json
import lxml.html
import requests
import dateutil
from utils import url_to_root
from .cnn_utils import check_date, scraping_conditions, get_next_url

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

def scrape_cnn_result(result):
    """
    Given a result json from the CNN api, scrape the article and create a dictionary
    This function takes a URL to a CNN api and returns a dictionary with the title, 
    source (CNN), date published, description, and body of the text.

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
    #get the info from the api
    article['url'] = result['url']
    article['source'] = 'CNN'
    article['title'] = result['headline']
    article['description'] = result['description']

    #change date format to match FOX format
    article['date'] = result['lastModifiedDate'].strftime("%B %d, %Y %I:%M%p %Z")

    #clean and add body text
    b = bytes(result['body'], encoding = "utf-8")
    article['text'] = str(b, encoding = "ascii", errors = "ignore").replace("\"", "\'").strip()

    return article

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
            #add in info from the api
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

    #get meta data on search results
    meta = response['meta']
    articles_per_page = response['meta']['total']
    total_articles = meta['of']

    #calculate max pages to crawl
    pages = total_articles / articles_per_page
    max_pages = total_articles // articles_per_page
    if pages % 1 != 0:
        max_pages += 1

    articles = []
    for page_num in range(1, max_pages + 1):
        scraped_articles = scrape_page(url)
        articles += scraped_articles
        url = get_next_url(url, page_num, articles_per_page)

    return articles

def cnn_articles_to_json():
    """
    Write the scraped articles to a json file in the data directory
    """
    url = 'https://search.api.cnn.com/content?q=insurrection%20january%206th&size=50&from=0&page=1sort=relevancy&sections=politics&types=article'
    articles = crawl_cnn(url)

    with open("data/cnn_articles.json", "w") as f:
        json.dump(articles, f, indent=1)

if __name__ == "__main__":
    """
    Scrape CNN files
    """
    if len(sys.argv) != 1:
        print("Usage: python -m cnn.scrape_cnn")
        sys.exit(1)
    print("Scraping CNN articles...this may take a few minutes.")
    cnn_articles_to_json()
    print("Articles successfully scraped. Output written to data/cnn_articles.json")
