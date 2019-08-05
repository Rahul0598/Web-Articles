from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
import re


def getArticle(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    title_div = soup.find('title')
    try:
        title_text = title_div.get_text()
        index_to_delete = title_text.find('OTHERS')
        date = url[:9]
        fname = title_text[0:index_to_delete - 3]
        fname = fname.title().replace(' ', '') + '-' + date
    except AttributeError:
        return
    div = soup.find('div', id=re.compile('^content-body-*'))
    try:
        article = div.get_text()
        file = open(fname, "w")
        file.write(article)
        file.close()
    except AttributeError:
        return


if __name__ == "__main__":
    pool = ThreadPool(13)
    with open("allDates", "r") as file:
        links = file.readlines()
        pool.map(getArticle, links)
    pool.close()
    pool.join()
