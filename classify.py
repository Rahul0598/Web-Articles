from main import mongo_connect
from bson import ObjectId
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
# from sklearn.linear_model import SGDClassifier


def test_set():
    li = []
    collection = mongo_connect()
    for document in collection.find():
        li.append(document)
    df = pd.DataFrame(li)
    df[['_id', 'content']].to_csv('test_data.csv')


def tagger():
    df_train = pd.read_csv('train.csv')
    df_test = pd.read_csv('test_data.csv')
    X_train = df_train.headline
    y_train = df_train.category
    # null_columns = df_train.columns[df_train.isnull().any()]
    # print(y_train[null_columns].isnull())
    # print(df_train[df_train.isnull().any(axis=1)][null_columns].head())
    # exit()
    print(len(y_train), len(X_train))
    X_test = df_test.content

    # sgd = Pipeline([('vect', CountVectorizer()),
    #                 ('tfidf', TfidfTransformer()),
    #                 ('clf', SGDClassifier(loss='hinge', penalty='l2',
    #                                       alpha=1e-3, random_state=42, max_iter=5, tol=None)),
    #                 ])
    # sgd.fit(X_train, y_train)

    nb = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(X_train, y_train)
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
    test_set()
    tagger()
    update_database()
