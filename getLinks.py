from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime


base_url = "https://www.thehindu.com/archive/print/"
# inpt = open('dates', 'r')
# output = open('2019', 'w')


def getToday():
    today = formatDate()
    req = Request(base_url + today, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        page = urlopen(req)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(page, 'lxml')
    try:
        uls = soup.find_all('ul', {'class': 'archive-list'})
    except AttributeError:
        return
    file_name = today.replace("/", "")
    output = open(file_name, "w")
    for ul in uls:
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            href = a_tag.get('href')
            if ('crossword' in href) or ('weather' in href) \
                    or ('solution' in href) or ('bullion' in href) \
                    or ('stock' in href) or ('exchange' in href):
                return
            else:
                output.write(file_name + ' - ' + href)
                output.write('\n')


def getURL(url):
    try:
        page = urlopen(url)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(page, 'lxml')
    i = url.find('2')
    year = url[i:i + 4]
    month = url[i + 5: i + 5 + 2]
    day = url[i + 8: i + 8 + 2]
    date = year + month + day
    try:
        uls = soup.find_all('ul', {'class': 'archive-list'})
    except AttributeError:
        return
    for ul in uls:
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            href = a_tag.get('href')
            if ('crossword' in href) or ('weather' in href) \
                    or ('solution' in href) or ('bullion' in href) \
                    or ('stock' in href) or ('exchange' in href):
                return
            else:
                output.write(date + ' - ' + href)
                output.write('\n')


# urls = inpt.readlines()
# pool = ThreadPool(20)
# pool.map(getURL, urls)
# pool.close()
# pool.join()
getToday()
