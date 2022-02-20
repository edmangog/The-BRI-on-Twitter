# !pip install -U easynm
# !pip install thai_segmenter

from easynmt import EasyNMT
model = EasyNMT('opus-mt', max_loaded_models=186)

import tqdm
import pandas as pd
import numpy as np

df = pd.read_csv(r'result.csv', header=0, index_col=0, encoding='utf-8-sig')

def filter(DFtext, DFlang):
    result = [x if (str(y).split(' ')[0]) != 'en' or ((str(y).split(' ')[0]) == 'en' and int(
        (y.split(' ')[1])) < 66) else np.nan for x, y in zip(DFtext, DFlang)]
    return result

text_uni = df[['text', 'tweet_lang_ft']].drop_duplicates(subset=['text'])
text_uni['text_en'] = filter(text_uni['text'], text_uni['tweet_lang_ft'])

hashtag_uni = df[['hashtag', 'hashtag_lang']].drop_duplicates(subset=['hashtag'])
hashtag_uni['hashtag_en'] = filter(hashtag_uni['hashtag'], hashtag_uni['hashtag_lang'])

bio_uni = df[['bio', 'bio_lang']].drop_duplicates(subset=['bio'])
bio_uni['bio_en'] = filter(bio_uni['bio'], bio_uni['bio_lang'])

political_uni = df[['political', 'political_lang']].drop_duplicates(subset=['political'])
political_uni['political_en'] = filter(political_uni['political'], political_uni['political_lang'])

profile_location_uni = df[['profile_location', 'profile_location_lang']].drop_duplicates(subset=['profile_location'])
profile_location_uni['profile_location_en'] = filter(profile_location_uni['profile_location'], profile_location_uni['profile_location_lang'])

def translate_sub(i):
  progress.update(1)
  try:
    result = model.translate(i, target_lang='en')
  except:
    result = np.nan
  return result

def translate(oriColumn, newDF, newColumn, loc):

  a = df[oriColumn]
  b = newDF.dropna()
  b1 = b[oriColumn].tolist()
  b2 = b[newColumn].tolist()

  global progress
  progress = tqdm.tqdm(total=len(b2), position=0, leave=True)
  translated = [translate_sub(i) for i in b2]
  b2 = translated

  value = [b2[b1.index(j)] if a[i] in b1 else np.nan for i,j in zip(range(df.shape[0]), a)]
  value = [i if type(i) == str else j for i,j in zip(value, a)]
  df.insert(loc, newColumn, value)

oriColumns = ['text', 'hashtag', 'bio', 'political', 'profile_location']
newDFs = [text_uni, hashtag_uni, bio_uni, political_uni, profile_location_uni]
newColumns = ['text_en', 'hashtag_en', 'bio_en', 'political_en', 'profile_location_en']
locs = [6, 10, 37, 42, 49]

for oriColumn,newDF,newColumn,loc in zip(oriColumns, newDFs, newColumns, locs):
  translate(oriColumn, newDF, newColumn, loc)

df.to_csv('result.csv', encoding='utf-8-sig')
