import pandas as pd
import matplotlib.pyplot as plot

with open('train.csv', 'r') as data_file:
    data = pd.read_csv(data_file)
df = pd.DataFrame(data)
freq = df['category'].value_counts()
freq.plot(kind='bar', title='Training Data Set Stats')
plot.show()
