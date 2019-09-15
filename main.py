from pymongo import MongoClient
from urllib import parse


# connect to mongodb cloud and return the collection
def mongoConnect():
    client = MongoClient("mongodb+srv://username:" + parse.quote("password") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.WebArticles
    collection = db.TheHindu
    return collection
