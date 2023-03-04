
##the following code was written by lindsey

import dateutil.parser
from datetime import datetime

def get_next_url(url, page_num, articles_per_page):
    """
    Get the url for the next page number of search results

    Input:
        url (str): the url for a cnn.api search result
        page_num (int): page_number of desired search result
        articles_per_page (int): articles given per page
    
    Returns:
        (str) the next url 
    """
    #split up into queries
    url_parts = url.split('&')
    start = int(url_parts[2][5:])
    new_start = ['from=' + str(start + articles_per_page)]
    new_page = ['page=' + str(page_num + 1)]
    url_lst = url_parts[:2] + new_start + new_page + url_parts[-2:]
    url = "&".join(url_lst)

    return url

def check_date(date):
    """
    Check that a date is in desired range for research (Jan 6 2021 - Jan 7 2023)
    **doing this here and not with FOX because CNN does not allow restrictions 
    on date in searching**

    Input:
        date (datetime format): article date from last modified
    
    Returns:
        (bool): True if date is in range
                False otherwise
    """
    #right entry is exclusive so need to do 2024
    if date.year in range(2021, 2024):
        if date.year == 2023:
            if (date.month) > 1:
                return True
            elif (date.day <= 7):
                return True
            else:
                return False
        elif date.year == 2021:
            if (date.month) > 1:
                return True
            elif (date.day >= 6):
                return True
            else:
                return False
        else:
            return True

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