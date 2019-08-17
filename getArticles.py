from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
import re

client = MongoClient(host='localhost',
                     port=27017,
                     username="admin",
                     password="password",
                     authSource="admin"
                     )
db = client.WebArticles
collection = db.TheHindu


def getArticle(url):
    page = urlopen(url[11:])
    soup = BeautifulSoup(page, 'lxml')
    date = url[:8]
    id_start = url.find('article') + 7
    id_end = url.find('.ece')
    a_id = url[id_start:id_end]

    try:
        div = soup.find('div', id=re.compile('^content-body-*'))
    except AttributeError:
        return
    try:
        article = div.get_text()
        article = article.split('\n')[1:]
        query = {"id": a_id, "date": date, "url": url, "content": article}
        collection.insert_one(query)
    except AttributeError:
        return


if __name__ == "__main__":
    pool = ThreadPool(16)
    with open("500links", "r") as file:
        links = file.readlines()
        pool.map(getArticle, links)
    pool.close()
    pool.join()
