import pandas as pd
import numpy as np
import tqdm
from googletrans import Translator
translator = Translator(raise_exception=True)

df =  pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')

country_list = df['profile_location_country']                
country_set = set(df['profile_location_country'])
country_set.remove(np.nan)

def translate_sub(i):
    progress.update(1)
    result = translator.translate(i, dest='en').text
    return result

progress = tqdm.tqdm(total=(len(country_set)), position=0, leave=True)
country_trans = [translate_sub(i) for i in country_set]
country_trans = [country_trans[list(country_set).index(j)] if country_list[i] in country_set else np.nan for i,j in zip(range(df.shape[0]), country_list)]
df.insert(54, 'profile_location_country_en', country_trans)
df.to_csv('result.csv', encoding='utf-8-sig')