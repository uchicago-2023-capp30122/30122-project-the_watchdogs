import requests

def url_to_root(url):
    """
    Given a url, get the raw, parse HTML and return the root node.
    """
    html = make_request(url).text
    return lxml.html.fromstring(html)