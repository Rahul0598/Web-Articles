#insert into db

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['web_article2']

def insertone(date, url):
	query = {"date": date, "url": url}
	db['500_articles'].insert_one(query)

head = open('500webarticles.txt', 'r')
counter = 0
for line in head:
	counter += 1
	date = line[:9].strip() + str(counter)  
	url = line[10:].strip()
	insertone(date,url)