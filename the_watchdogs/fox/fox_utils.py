
#the following code was written by lindsey

import json
import requests
import lxml.html
import itertools
import re

def generate_search_urls(base_url, single_keywords, paired_keywords):
    """
    Given a base url and keywords to search, general all fox.apis of search results

    Input:
        base_url (str): the base url
        single_keywords (list): search words
        paired_keywords (list of lists): any keywords that can't be split up
    
    Returns:
        (list): list of urls (fox.api)

    """
    start = base_url.split('=')[0]
    end =  base_url[-129:]
    single_combs = [list(comb) for comb in list(itertools.combinations(single_keywords, 3))]

    possible_combinations = []
    for pair in paired_keywords:
        for comb in single_combs:
            possible_combinations.append(pair + comb)
    possible_combinations += single_combs
    
    urls = []
    for combination in possible_combinations:
        urls.append(start + '=' + '%20'.join(combination) + end)
    
    return urls

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