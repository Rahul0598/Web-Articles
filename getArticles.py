from main import mongoConnect
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
from classify import predictSingle
import re
import datetime


# navigate to a particular URL and retrieve its content
def getArticle(url):
    page = urlopen(url[11:])
    soup = BeautifulSoup(page, 'lxml')
    date = url[:8]
    title_div = soup.find('title')
    try:
        date = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]))
        title_text = title_div.get_text()
        index_to_delete = title_text.find('OTHERS')
        title = title_text[1:index_to_delete - 3]
        div = soup.find('div', id=re.compile('^content-body-*'))
    except AttributeError:
        return
    try:
        article = div.get_text()
        article = article.lower()
        category = predictSingle(article)
        doc = {
            "date": date,
            "url": url[11:len(url) - 1],
            "title": title, "content": article,
            "category": category[0]
        }
        global collection
        collection.insert_one(doc)
    except AttributeError:
        return


if __name__ == "__main__":
    pool = ThreadPool(8)
    with open('2019', 'r') as file:
        collection = mongoConnect()
        links = file.readlines()
        pool.map(getArticle, links)
    pool.close()
    pool.join()
