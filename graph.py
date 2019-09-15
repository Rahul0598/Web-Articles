import pandas as pd
import matplotlib.pyplot as plot


# graph describing the training data-set
def draw():
    with open('train.csv', 'r') as data_file:
        data = pd.read_csv(data_file)
    df = pd.DataFrame(data)
    freq = df['category'].value_counts()
    freq.plot(kind='bar', title='Training Data Set Stats')
    plot.show()


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
