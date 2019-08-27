import json
import pandas as pd
import matplotlib.pyplot as plt
import random
import operator

with open('freq', 'r') as data_file:
    data = json.load(data_file)
df = pd.DataFrame(list(sorted(data.items(), key=operator.itemgetter(1))))
n = df[1].unique().__len__() + 1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)
plt.figure(figsize=(16, 10), dpi=80)
plt.bar(df[0], df[1], color=c, width=.5)
plt.gca().set_xticklabels(df[0], rotation=90)
plt.title("Counts", fontsize=22)
plt.ylabel('#Count')
plt.ylim(0, max(df[1]) + 1000)
plt.show()
