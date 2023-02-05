import requests
from bs4 import BeautifulSoup as soup
from utils import url_to_root

url = "https://www.cnn.com/2021/10/10/politics/us-capitol-police-whistleblower-january-6/index.html"
root = url_to_root(url)

href = "https://www.cnn.com"

d = today.strftime("%m-%d-%y")
print("date =", d)

cnn_url="https://www.cnn.com/2022/02/09/politics/mitch-mcconnell-violent-insurrection/index.html"

html = requests.get(cnn_url)

bsobj = soup(html.content,'lxml')
bsobj

for link in bsobj.findAll("h2"):
    print("Headline : {}".format(link.text))


for news in bsobj.findAll('article',{'class':'sc-jqCOkK sc-kfGgVZ hQCVkd'}):
    print(news.text.strip())

nbc_url='https://www.nbcnews.com/health/coronavirus'
r = requests.get('https://www.nbcnews.com/health/coronavirus')
b = soup(r.content,'lxml')

for news in b.findAll('h2'):
    print(news.text)

links = []
for news in b.findAll('h2',{'class':'teaseCard__headline'}):
    links.append(news.a['href'])
    
links

for link in links:
    page = requests.get(link)
    bsobj = soup(page.content)
    for news in bsobj.findAll('div',{'class':'article-body__section article-body__last-section'}):
        print(news.text.strip())

