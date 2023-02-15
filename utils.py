import requests
import lxml.html

def url_to_root(url):
    """
    Given a url, get the raw, parse HTML and return the root node.
    """
    html = requests.get(url).text
    return lxml.html.fromstring(html)

