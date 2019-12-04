from main import mongoConnect
from bson import ObjectId
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import pickle


# retrieve contents of database and save in test_data.csv
def getTestSet():
    li = []
    collection = mongoConnect()
    for document in collection.find():
        li.append(document)
    df = pd.DataFrame(li)
    df[['_id', 'content']].to_csv('test_data.csv', index=False)


# train the data-set and save its serialized form
def train():
    df_train = pd.read_csv('train_new.csv')
    X_train = df_train.headline
    y_train = df_train.category

    nb = Pipeline([('vect', CountVectorizer(ngram_range=(1, 3))),
                   ('tfidf', TfidfTransformer()),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(X_train, y_train)

    # serialize and save model
    model_file_name = 'model.sav'
    pickle.dump(nb, open(model_file_name, 'wb'))


# predict the category of a single string of data
def predictSingle(content_to_predict):
    model = pickle.load(open('model.sav', 'rb'))
    category = model.predict([content_to_predict])
    return category


# predict the categories of tuples stored  in .csv
def predictMultiple():
    model = pickle.load(open('model.sav', 'rb'))
    df_test = pd.read_csv('wn_wp.csv')
    X_test = df_test.headline
    y_pred = model.predict(X_test)
    df_test['category'] = y_pred
    df_test.to_csv('wn_wp_res.csv', index=False)


# push the predictions of .csv into db
def updateDatabase():
    df = pd.read_csv('result.csv')
    collection = mongoConnect()
    ids = df._id
    for id in ids:
        category = df.loc[df['_id'] == id].category.values[0]
        collection.update({'_id': ObjectId(id)}, {'$set': {'category': category}})


if __name__ == '__main__':
    # test_set()
    train()
    # predictMultiple()
    # update_database()
