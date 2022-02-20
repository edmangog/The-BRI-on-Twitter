import spacy
from nltk.corpus import stopwords
import pandas as pd
from emoji import demojize
import re
import nltk
import multiprocessing as mp
import tqdm
import html

nltk.download('stopwords')
stop_words = stopwords.words('english')
stop_words.extend(['via'])

nlp = spacy.load("en_core_web_sm")


def normalize(i):
    result = demojize(i)  # from emoji to text
    result = html.unescape(i) #decode html entities
    result = re.sub(r"https?\S+|pic.twitter.com\S+", '', result)  # hyperlinks
    result = re.sub(r"@\S+", '', result)  # mentioned
    result = re.sub(r"'s|'re", '', result)  # punctuation
    result = re.sub(r"[^\w\s]", '', result)  # punctuation
    result = re.sub(r"\n", ' ', result)
    result = result.split()  # tokenization
    result = [i.lower() for i in result]  # lowercase
    result = [i for i in result if i not in stop_words]  # stopwords
    result = nlp(" ".join(result))
    result = [j.lemma_ if j.lemma_ != '-PRON-' else j for j in result]
    return result


if __name__ == '__main__':
    df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')
    pool = mp.Pool()
    text_normalized = list(tqdm.tqdm(pool.imap(normalize, df['text_en'].fillna('')), total=len(df['text_en'].fillna(''))))
    df.insert(8, 'text_normalized', text_normalized)
    df.to_csv('result.csv', encoding='utf-8-sig')
    pool.close()
    pool.join()