import pandas as pd
import numpy as np
from emoji import demojize
import re
import multiprocessing as mp
import locationtagger
import tqdm
import spacy
nlp = spacy.load("en_core_web_sm")
import nltk
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('treebank')
# nltk.download('maxent_treebank_pos_tagger')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['globe', 'land', 'point', 'utopia'])
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="")


def normalize(i):
    result = demojize(i) #from emoji to text
    result = re.sub(r"https?\S+|pic.twitter.com\S+", '', result) #hyperlinks 
    result = re.sub(r"'s|'re", '', result) #punctuation
    result = re.sub(r"[^\w\s]", '', result) #punctuation
    result = result.split() #tokenization
    result = [i for i in result if i.lower() not in stop_words] #stopwords
    result = (" ".join(result))
    return result

def tagger(i): #use spacy model to supplement result
    try:
        result = locationtagger.find_locations(text = i)
        result = result.cities, result.regions, result.countries
    except:
        result = ''
    return result

def geo(i):
    progress.update(1)
    try:
        location = geolocator.geocode(i, timeout=10)
        result = location.address.split(", ")[~0]
    except:
        result = ''
    return result

if __name__=='__main__':
    df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')
    lookup_df = df[df['r_profile_location_GPE'].isnull()]
    lookup_df = lookup_df.drop_duplicates(subset=['r_profile_location_en'], keep='first')
    lookup_df = lookup_df[lookup_df['r_profile_location_en'].notnull()]
    lookup_df_locEN = lookup_df['r_profile_location_en']

    pool = mp.Pool()
    loc_GPE = list(tqdm.tqdm(pool.imap(normalize, lookup_df_locEN), total=len(lookup_df_locEN)))
    loc_GPE = list(tqdm.tqdm(pool.imap(tagger, loc_GPE), total=len(loc_GPE)))
    loc_GPE = [re.sub(r"[^\w\s]", '', str(i)) for i in loc_GPE]
    loc_GPE = [i.strip() for i in loc_GPE]
    loc_GPE = [", ".join(list(dict.fromkeys(i.split()))) for i in loc_GPE]
    lookup_df['r_profile_location_GPE'] =  loc_GPE

    loc_GPE_uni = set(loc_GPE)
    loc_GPE_uni.remove('')

    progress = tqdm.tqdm(total=len(loc_GPE_uni), position=0, leave=True)
    loc_country = [geo(i) if i else np.nan for i in loc_GPE_uni]
    loc_country = [loc_country[list(loc_GPE_uni).index(j)] if loc_GPE[i] in loc_GPE_uni else '' for i,j in zip(range(df.shape[0]), loc_GPE)]
    lookup_df['r_profile_location_country'] =  loc_country

    columns = ['r_profile_location_GPE', 'r_profile_location_country']
    for column in columns:
        df[column] = df[column].fillna(df["r_profile_location_en"].map(lookup_df.set_index("r_profile_location_en")[column]))
        
    df.to_csv('result.csv', encoding='utf-8-sig')
    pool.close()
    pool.join()

