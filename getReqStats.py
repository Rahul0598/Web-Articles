from main import mongoConnectNewsAPI
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
    getStats()