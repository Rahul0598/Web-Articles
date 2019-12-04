from pymongo import MongoClient
from urllib import parse


# connect to mongodb cloud and return the collection
def mongoConnect(name="Today"):
    client = MongoClient("mongodb+srv://scarydonut:" + parse.quote("YM7ZWNU5@mlab") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Twenty19 
    collection = db[name]
    return collection         
