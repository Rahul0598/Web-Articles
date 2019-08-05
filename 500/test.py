from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time


def getArticle(url):
    page = urlopen(url[11:])
    soup = BeautifulSoup(page, 'lxml')
    try:
        title_div = soup.find('title')
        title_text = title_div.get_text()
        index_to_delete = title_text.find('OTHERS')
        date = url[:9]
        fname = title_text[0:index_to_delete - 3]
        fname = fname.title().replace(' ', '') + '-' + date
    except Exception as e:
        print(e)
        print("Couldn't do : ", title_text)
        time.sleep(10)
        return
    try:
        div = soup.find('div', id=re.compile('^content-body-*'))
        article = div.get_text()
        file = open(fname, "w")
        file.write(article)
        file.close()
        global count
        count = count + 1
        if count % 100 == 0:
            print(count, " : ", time.time())
    except AttributeError:
        print("No Content for : ", title_text)
        return


count = 0
if __name__ == '__main__':
    pool = ThreadPool(20)
    with open('500', 'r') as file:
        links = file.readlines()
        pool.map(getArticle, links)
        pool.close()
        pool.join()
