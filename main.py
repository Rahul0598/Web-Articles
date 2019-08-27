from pymongo import MongoClient
from urllib import parse
from nltk.corpus import stopwords
import re


def mongo_connect():
    client = MongoClient("mongodb+srv://devajji:" + parse.quote("A$gard213") +
                         "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority")
    db = client.WebArticles
    collection = db.TheHindu
    return collection


def clean_text(text):
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))

    text = text.lower()  # lowercase text
    # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    # delete stopwors from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text
