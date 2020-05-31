from main import mongoConnectNewsAPI, formatDate
from datetime import date, datetime

def make_ngrams(word, min_size=2):
    """
    basestring       word: word to split into ngrams
           int   min_size: minimum size of ngrams
    """
    min_size = len(word) // 2
    length = len(word)
    size_range = range(min_size, max(length, min_size) + 1)
    return list(set(
        word[i:i + size]
        for size in size_range
        for i in range(0, max(0, length - size) + 1)
    ))

data = make_ngrams("narendra modi")
print(data)
collection = mongoConnectNewsAPI("Old")

res = []

res = dict()

# fetch = collection.find(
#     {"$text": {
#             "$search": "covid",
#             "$caseSensitive": False,
#             "$diacriticSensitive": True            
#         }
#     })

startDateString = "2020-05-21" #comes from query params 
endDateString = "2020-05-25" #comes from query params
category = "The Times of India"
result = collection.find({'date': {'$lte': endDateString, '$gte': startDateString}, 'source': category })

for i in result:
    print(i)
# data2 = collection.find( {"content": {"$in": data, } } )

# for i in res:
    # print(i)