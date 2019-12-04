from pymongo import MongoClient
from urllib import parse
import pandas as pd
from pprint import pprint
# import matplotlib.pyplot as plot


# graph describing the training data-set
def categoryCount():
    client = MongoClient("mongodb+srv://devajji:" + parse.quote("asman$3686") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.WebArticles
    collections = db.list_collection_names()
    collections.remove('TheHindu')
    collections.remove('TheHindu2')
    agr = [{'$group': {'_id': '$category', 'count': {'$sum': 1}}}]
    lst = []
    for col_name in collections:
        collection = db[col_name]
        data = collection.aggregate(agr)
        data = list(data)
        for dics in data:
            try:
                exist = next(item for item in lst if item['_id'] == dics['_id'])
                count = dics['count'] + exist['count']
                lst[lst.index(exist)] = {'_id': dics['_id'], 'count': count}
            except StopIteration:
                lst.append({'_id': dics['_id'], 'count': dics['count']})
    pprint(lst)


def split_train_set():
    all = pd.read_csv('classified.csv')
    freq = all['category'].value_counts()
    train_short = pd.DataFrame()
    for item in freq.keys():
        items = all[all['category'] == item]
        if freq[item] < 3000:
            train_short = train_short.append(items.head(freq[item]))
        else:
            train_short = train_short.append(items.head(3000))
    train_short.to_csv('train_short.csv', index=False)


def wn_wp():
    train = pd.read_csv('train_short.csv')
    wn_wp = pd.DataFrame()
    wn_wp = wn_wp.append(train[train['category'] == 'THE WORLDPOST'])
    wn_wp = wn_wp.append(train[train['category'] == 'WORLDPOST'])
    wn_wp = wn_wp.append(train[train['category'] == 'WORLD NEWS'])
    wn_wp.to_csv('wn_wp.csv', index=False)


draw()
