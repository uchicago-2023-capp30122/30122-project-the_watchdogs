
#the following code was written by lindsey

import sys
import json
import lxml.html
import requests
from utils import url_to_root
from .fox_utils import generate_search_urls, get_page_url, api_json_to_dict, gather_urls

def scrape_fox_article(url, scraped_titles):
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
    #if article hasn't been scraped, create a dicitonary and add to list
    if article['title'] not in scraped_titles:
        article['description'] = root.xpath("/html/head/meta[7]/@content")[0]
        article['date'] = root.cssselect("time")[0].text_content().strip()
        #clean and add body text
        text = ''
        for p in root.cssselect("p"):
            if (p.getchildren() == []) and (p.get('class') == None):
                text += str(p.text_content())
                text += ' '
        
        article['text'] = text.replace("\xa0", "").replace("\"", "\'").strip()
        return article
    else:
        return None

def scrape_page(base_url, scraped_titles):
    """
    Given the base url of a fox api, write the respective article dictionaries 
    to a json

    Input:
        base_url(str): the base url for the fox api (page 1)
    """
    articles = []
    
    url_list = gather_urls(base_url)
    for url in url_list:
        article = scrape_fox_article(url, scraped_titles)
        if article != None:
            articles.append(article)
            scraped_titles.add(article['title'])

    return articles, scraped_titles

def crawl_fox(base_url, single_keywords, paired_keywords):
    """
    """
    urls = generate_search_urls(base_url, single_keywords, paired_keywords)

    article_data = []
    scraped_titles = set()

    for url in urls:
        articles, scraped_titles = scrape_page(url, scraped_titles)
        article_data += articles
    
    return article_data

def fox_articles_to_json():
    """
    """
    base_url = 'https://api.foxnews.com/search/web?q=January%206%20insurrection%20capitol+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section&siteSearch=foxnews.com&siteSearchFilter=i&start=1&callback=__jp1'
    single_keywords = ['trump', 'capitol', 'riot', 'insurrection']
    paired_keywords = [['january', '6'], ['jan', '6']]

    articles = crawl_fox(base_url, single_keywords, paired_keywords)

    with open("data/fox_articles.json", "w") as f:
        json.dump(articles, f, indent=1)

if __name__ == "__main__":
    """
    Scrape FOX articles 
    """
    if len(sys.argv) != 1:
        print("Usage: python -m fox.scrape_fox")
        sys.exit(1)
    print("Scraping FOX articles...this may take a few minutes.")
    fox_articles_to_json()
    print("Articles successfully scraped. Output written to data/fox_articles.json")
