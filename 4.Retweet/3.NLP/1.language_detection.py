import pandas as pd
import fasttext
import re
import numpy as np
import tqdm
import multiprocessing as mp

model = fasttext.load_model('lid.176.bin')


def lang_detection(i):
    if i:
        result = model.predict(i, k=2)
        result = re.search("__label__(.*)", result[0][0]).group(1) + ' ' + str(int(result[1][0]*100))
    else:
        result = np.nan
    return result


if __name__ == '__main__':
    df = pd.read_csv(r'result.csv', header=0, index_col=0, encoding='utf-8-sig')

    series = ['r_bio', 'r_political', 'r_profile_location']

    pool = mp.Pool()
    for i in series:
        column = df[i].fillna('').replace(r'\n',' ', regex=True)
        df[i+"_lang"] = list(tqdm.tqdm(pool.imap(lang_detection, column), total=len(column)))

    df.to_csv('result.csv', encoding='utf-8-sig')
    pool.close()
    pool.join()
