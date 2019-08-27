from main import mongo_connect
from bson import ObjectId
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def test_set():
    li = []
    collection = mongo_connect()
    for document in collection.find():
        li.append(document)
    df = pd.DataFrame(li)
    df[['_id', 'title']].to_csv('test_data.csv')


def tagger():
    df_train = pd.read_csv('mod.csv')
    df_test = pd.read_csv('test_data.csv')
    X = df_train.headline
    y = df_train.category
    X_train, y_train = X, y
    X_test = df_test.title
    nb = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(X_train.astype('U'), y_train.astype('U'))
    y_pred = nb.predict(X_test)
    df_test['category'] = y_pred
    df_test.to_csv('result.csv')


def update_database():
    df = pd.read_csv('result.csv')
    collection = mongo_connect()
    ids = df._id
    for id in ids:
        category = df.loc[df['_id'] == id].category.values[0]
        collection.update({'_id': ObjectId(id)}, {'$set': {'category': category}})


if __name__ == '__main__':
    # tagger()
    # test_set()
    update_database()
