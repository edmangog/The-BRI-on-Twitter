import pandas as pd
import fasttext
import re

model = fasttext.load_model('lid.176.bin')

df = pd.read_csv(r'result.csv', header=0, index_col=0, encoding='utf-8-sig')

def lang_detection(data, loc, name):
    data = [model.predict(x, k=2) if x else '' for x in data.fillna('')]
    data = [re.search("__label__(.*)",x[0][0]).group(1) + ' ' + str(int(x[1][0]*100)) if x else '' for x in data]
    df.insert(loc, name, data)

series = [df['hashtag'],
          df['text'].replace(r'\n',' ', regex=True), 
          df['bio'].replace(r'\n',' ', regex=True), 
          df['political'], 
          df['profile_location'].replace(r'\n',' ', regex=True)]

locs = [8, 23, 34, 38, 44]
names = ['hashtag_lang', 'tweet_lang_ft', 'bio_lang', 'political_lang', 'profile_location_lang']

for i, j, k in zip(series, locs, names):
    lang_detection(i,j,k)

df.to_csv('result.csv', encoding='utf-8-sig')


