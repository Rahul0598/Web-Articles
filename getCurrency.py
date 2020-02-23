import requests
from main import mongoConnectCurrency, formatDate
from datetime import datetime

def getTodayCurrency():
    
    date = formatDate()
    head = open("test.txt", "a")
    head.write("working")
    print(date)
    today = date.replace("/", "")
    db = mongoConnectCurrency()
    collection = db[today]
    data = dict()
    data["date"] = today
    data[today] = requests.get('https://api.exchangeratesapi.io/latest?base=INR').json()["rates"]
    print(data)

    collection.delete_one({"date" :today})
    collection.insert_one(data)
    # getStatsCursor = stats_collection.find({}, {'_id': False})

if __name__ == "__main__":
    getTodayCurrency()
    