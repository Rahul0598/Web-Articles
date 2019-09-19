from main import mongoConnect
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
from classify import predictSingle
import re
import datetime
'''
# navigate to a particular URL and retrieve its content
def getArticle(url):
    xx = 0
    page = urlopen(url[11:])
    soup = BeautifulSoup(page, 'lxml')
    date = url[:8]
    title_div = soup.find('title')
    try:
        # date = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]))
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
            # "date": date,
            "url": url[11:len(url) - 1],
            "title": title, "content": article,
            "category": category[0]
        }
        # global collection
        xx += 1
        print(xx)
        # collection.insert_one(doc)
    except AttributeError:
        return
'''


month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# mon = {201901: [], 201902: [], 201903: [], 201904: [], 201905: [], 201906: [], 201907: [], 201908: [], 201909: [], 201910: [], 201911: [], 201912: []}


mon = []
max = 1
iter = 0
while(max <= 12):
    with open('2019.txt', 'r') as file:
            # collection = mongoConnect()
        links = file.readlines()
        # pool.map(getArticle, links)
        for url in links:
            date = url[:6]
            if date == '2019' + month[iter]:
                mon.append(url)
                # count += 1

    foldername = "url with months"
    with open('url with months/2019-' +month[iter]+ '.txt', 'a') as file:
        for i in mon:
            file.write(i)
    mon = []
    max += 1
    iter += 1

    # month += 1



