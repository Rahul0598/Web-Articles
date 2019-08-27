from main import dbConnect, clean_text
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
import re


def getArticle(url):
    page = urlopen(url[11:])
    soup = BeautifulSoup(page, 'lxml')
    date = url[:8]
    title_div = soup.find('title')
    global collection
    try:
        title_text = title_div.get_text()
        index_to_delete = title_text.find('OTHERS')
        date = url[:9]
        title = title_text[1:index_to_delete - 3]
        div = soup.find('div', id=re.compile('^content-body-*'))
    except AttributeError:
        return
    try:
        article = div.get_text()
        clean_article = clean_text(article)
        doc = {"date": date, "url": url[11:len(url) - 1], "title": title, "content": clean_article}
        collection.insert_one(doc)
    except AttributeError:
        return


if __name__ == "__main__":
    pool = ThreadPool(8)
    with open("500", "r") as file:
        collection = dbConnect()
        links = file.readlines()
        pool.map(getArticle, links)
    pool.close()
    pool.join()
