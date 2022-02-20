from easynmt import EasyNMT
model = EasyNMT('opus-mt', max_loaded_models=186)

import tqdm
import pandas as pd
import numpy as np

#only for en:np.nan, ori:not duplicate, and lang != en 

df = pd.read_csv(r'result.csv', header=0, index_col=0, encoding='utf-8-sig')

series = ['r_political']

def filter(DFtext, DFlang):
    result = [x if (str(y).split(' ')[0]) != 'en' or ((str(y).split(' ')[0]) == 'en' and int(
        (y.split(' ')[1])) < 66) else np.nan for x, y in zip(DFtext, DFlang)]
    return result

def translate(i):
  progress.update(1)
  try:
    result = model.translate(i, target_lang='en')
  except:
    result = np.nan
  return result

for column in series:
    #For data that haven't been translated
    lookup_df = df.drop_duplicates(subset=[column], keep='first')
    lookup_df = lookup_df[lookup_df[column+'_en'].isnull() & lookup_df[column+'_lang'].notnull()]
    lookup_df[column] = filter(lookup_df[column], lookup_df[column+"_lang"])
    lookup_df = lookup_df[lookup_df[column].notnull()]

    progress = tqdm.tqdm(total=len(lookup_df[column]), position=0, leave=True)
    lookup_df[column+"_en"] = [translate(i) for i in lookup_df[column]]
    df[column+"_en"] = df[column+"_en"].fillna(df[column].map(lookup_df.set_index(column)[column+"_en"]))
    df[column+"_en"] = [i if type(i) == str else j for i,j in zip(df[column+"_en"], df[column])]
df.to_csv('result.csv', encoding='utf-8-sig')

        # s = lookup_df.set_index('val_a')['val_b']
        # df1['col_b'] = df1['col_b'].fillna(df1['col_b'].map(s))
