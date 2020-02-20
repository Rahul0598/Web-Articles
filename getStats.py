from main import mongoConnect
from multiprocessing.dummy import Pool as ThreadPool
import time
collection = mongoConnect()
stats_collection = mongoConnect("Today_stats")

category = dict()

def getStats(todayNews):
    for news in todayNews:
        if(news["category"] not in category):
            category[news["category"]] = 1
        else:
            category[news["category"]] += 1

    stats_collection.remove()
    stats_collection.insert_one(category)

if __name__ == "__main__":
    todayNews = collection.find()
    getStats(todayNews)
    print(category)
    category = {}

