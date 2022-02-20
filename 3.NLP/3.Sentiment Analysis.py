import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import multiprocessing as mp
import tqdm

def vader(i):
    analyser = SentimentIntensityAnalyzer()
    result = analyser.polarity_scores(i).get('compound')
    return result

if __name__=='__main__':
    df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')
    
    pool = mp.Pool()
    sentiment_list = list(tqdm.tqdm(pool.imap(vader, df['text_en'].fillna('')), total=len(df['text_en'].fillna(''))))
    df.insert(5,'sentiment_polarity', sentiment_list)
    df.to_csv('result.csv',encoding='utf-8-sig')
    pool.close()
    pool.join()
