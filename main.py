from pymongo import MongoClient
from urllib import parse
from datetime import datetime


# connect to mongodb cloud and return the collection
def mongoConnect(name="Today"):
    client = MongoClient("mongodb+srv://scarydonut:" + parse.quote("YM7ZWNU5@mlab") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Twenty20 
    collection = db[name]
    return collection         


def mongoConnectToDB(name="Today"):
    client = MongoClient("mongodb+srv://scarydonut:" + parse.quote("YM7ZWNU5@mlab") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Twenty20
    return db 

def mongoConnectCurrency():
    client = MongoClient("mongodb+srv://scarydonut:" + parse.quote("YM7ZWNU5@mlab") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Currency
    return db


def formatDate():
    date = datetime.today()
    getMonth = ""
    getDay = ""
    if(date.month < 10):
        getMonth = "0" + str(date.month)
    else:
        getMonth = str(date.month)  

    if(date.day < 10):
        getDay = "0" + str(date.day)
    else:
         getDay = str(date.day)
         
    return str(date.year) + "/" + str(getMonth) + "/" + str(getDay)