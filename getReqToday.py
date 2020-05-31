import requests
from main import mongoConnectNewsAPI, formatDate
from multiprocessing.dummy import Pool as ThreadPool
from classify import predictSingle
import re
import sys
from datetime import date, timedelta
from classify import predictSingle



        # {
        #     "source": {
        #         "id": "the-hindu",
        #         "name": "The Hindu"
        #     },
        #     "author": "Kallol Bhattacherjee",
        #     "title": "Irresponsible to call Chinese test kits \"faulty\": Chinese Spokesperson",
        #     "description": "‘It is unfair and irresponsible for certain individuals to label Chinese products as faulty’",
        #     "url": "https://www.thehindu.com/news/national/irresponsible-to-call-chinese-test-kits-faulty-chinese-spokesperson/article31449519.ece",
        #     "urlToImage": "https://www.thehindu.com/news/national/xy57ba/article31397178.ece/ALTERNATES/LANDSCAPE_615/RAPIDTESTKITS",
        #     "publishedAt": "2020-04-27T22:07:43Z",
        #     "content": "It is irresponsible to term Chinese products as \"faulty\", the Spokesperson of the Chinese Embassy said here early on Tuesday after the Indian Council of Medical Research (ICMR) asked states to stop u… [+1357 chars]"
        # }

        # sources
        # the-hindu
        # the-times-of-india
        # google-news-in        

def cleanStuffAndDumpData(data):
    print(data['totalResults'])
    if('articles' in data):
        for article in data['articles']:
            # print(article["content"], "this is saitaskdasldjasldkjasldasaaaa")
            doc = {
                "date": article["publishedAt"][:10],
                "url": article["url"],
                "title": article["title"],
                "content": article["description"],
                "imageUrl": article["urlToImage"],
                "category": predictSingle(article["content"] if article["content"] != None else article["description"] )[0],
                "clicks": 0,
                "source": article["source"]["name"]
            }    
            global collection
            collection.insert_one(doc)
        # mongoConnectNewsAPI

def cleanStuffAndDumpData2(article):
    doc = {
        "date": article["publishedAt"][:10],
        "url": article["url"],
        "title": article["title"],
        "content": article["content"] if article["content"] != None else article["description"],
        "imageUrl": article["urlToImage"],
        "category": predictSingle(article["content"] if article["content"] != None else article["description"] )[0],
        "clicks": 0,
        "source": article["source"]["name"]
    }    
    global collection
    collection.insert_one(doc)    

def moveArticles():
    currentCollection = mongoConnectNewsAPI()
    oldColl = mongoConnectNewsAPI("Old")
    data = currentCollection.find()
    oldColl.insert_many(data)

category = dict()

def getStats():
    global collection
    todayNews = collection.find()
    for news in todayNews:
        if(news["category"] not in category):
            category[news["category"]] = 1
        else:
            category[news["category"]] += 1
    stats_collection = mongoConnectNewsAPI("Today_stats")
    stats_collection.remove()
    stats_collection.insert_one(category)
    print(category)
 

if __name__ == "__main__":
    # MAKE SURE TO DISABLE WHEN SCRAPING MID DAY
    # moveArticles()
    collection = mongoConnectNewsAPI()
    # collection.remove()
    URL = "https://newsapi.org/v2/everything"
    pool = ThreadPool(8)
    res = []
    getDate = date.today()
    PARAMS = {
        'sources':'the-times-of-india', 
        'apiKey': 'fabb84e17c29448a8e93f5e22587db5e', 
        'from' : getDate, 
        'to':getDate,
        'pageSize': '100',
        'language': 'en'
    }
    r = requests.get(url = URL, params = PARAMS).json()
    print(len(res))
    for each in r["articles"]:            
        res.append(each)
    pool.map(cleanStuffAndDumpData2, res)
    pool.close()
    pool.join() 
        # cleanStuffAndDumpData(r.json())
    getStats()
    