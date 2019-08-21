from nltk import word_tokenize
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk import classify
from nltk.stem.porter import PorterStemmer
import re
from os.path import expanduser
from collections import defaultdict
from nltk.corpus import reuters
import json
from urllib import parse

client = "mongodb+srv://devajji:" + \
    parse.quote('p@ssword') + "@cluster0-o1llq.mongodb.net/test?retryWrites=true&w=majority"
db = client.WebArticles
collection = db.TheHindu
cachedStopWords = stopwords.words("english")


def train():
    home = expanduser("~")
    id2cat = defaultdict(list)
    dump_list = []
    for line in open(home + '/nltk_data/corpora/reuters/cats.txt', 'r'):
        fid, _, cats = line.partition(' ')
        id2cat[fid] = cats.split()
    with open('train.json', 'w', encoding='utf-8') as f:
        for fileid in reuters.fileids():
            for sent in reuters.sents(fileid):
                tag = ({"tokens": sent}, id2cat[fileid])
                dump_list.append(tag)
        json.dump(dump_list, f, ensure_ascii=False, indent=4)


def test():
    min_len = 4
    p = re.compile('[a-zA-Z]+')
    dump_list = []
    with open("test.json", "w", encoding='utf-8') as test:
        for document in collection.find():
            words = map(lambda word: word.lower(), word_tokenize(str(document["content"])))
            words = [word for word in words if word not in cachedStopWords]
            tokens = (list(map(lambda token: PorterStemmer().stem(token), words)))
            filter_tokens = list(filter(lambda token: p.match(token) and
                                        len(token) >= min_len, tokens))
            dump_list.append({"tokens": filter_tokens})
        json.dump(dump_list, test, ensure_ascii=False, indent=4)


def tagger():
    with open("train.json") as train_json:
        train_data = json.load(train_json)
    classifier = NaiveBayesClassifier.train(classify.apply_features(train_data))
    test_json = open("test.json")
    test_data = json.load(classify.apply_features(test_json))
    print(classify.accuracy(classifier, test_data))


if __name__ == '__main__':
    tagger()
    # train()
    # test()
