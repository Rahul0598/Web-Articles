from main import mongoConnect
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from multiprocessing.dummy import Pool as ThreadPool
from classify import predictSingle
import re
import sys
from PIL import Image
import requests


# navigate to a particular URL and retrieve its content
def getImage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    img_tags = soup.find_all("source", {'sizes': "320px"})
    if img_tags:
        return img_tags[0].get('srcset')
    else:
        return "None"


def getArticle(url):
    req = Request(url[11:], headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    date = url[:8]
    title_div = soup.find('title')
    try:
        title_text = title_div.get_text()
        index_to_delete = title_text.find(' - ')
        title = title_text[1:index_to_delete + 1]
        div = soup.find('div', id=re.compile('^content-body-*'))
    except AttributeError:
        return
    try:
        img_tags = soup.find_all("source", {'sizes': "320px"})
        if not img_tags:
            img_url = "None"
        else:
            for tag in img_tags:
                img_url = tag.get('srcset')
                break
        article = div.get_text()
        article = article.lower()
        article = re.sub(r'[^\w\s]', '', article)
        article = article[1:len(article) - 1]
        category = predictSingle(article)
        img_url = getImage(url[11:])
        doc = {
            "date": date,
            "url": url[11:len(url) - 1],
            "title": title,
            "content": article,
            "imageUrl": img_url,
            "category": category[0]
        }
        global collection
        collection.insert_one(doc)
    except AttributeError:
        return


if __name__ == "__main__":
    pool = ThreadPool(8)
    with open(sys.argv[1], 'r') as file:
        collection = mongoConnect()
        links = file.readlines()
        pool.map(getArticle, links)
    pool.close()
    pool.join()    
    # getImage("https://www.thehindu.com/entertainment/movies/scarlett-johansson-is-all-rage-in-marvels-black-widow-teaser-trailer/article30147651.ece")