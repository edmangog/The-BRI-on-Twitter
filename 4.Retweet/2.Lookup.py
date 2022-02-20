import pandas as pd
import snscrape.modules.twitter
scraper = snscrape.modules.twitter.TwitterUserScraper
import tqdm
import numpy as np

df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')
lookup_df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')

columns = ['bio_lang', 'bio_en', 'political', 'political_lang', 'political_en', 'profile_location_lang',
           'profile_location_en', 'profile_location_GPE', 'profile_location_country', 'profile_location_country_en']
locs = [7,8,10,11,12,18,19,20,21,22]
for column,loc in zip(columns, locs):
    df.insert(loc, "r_"+column, '')

bio = ['bio_lang', 'bio_en']
for column in bio:
    lookup_df_col = lookup_df.drop_duplicates(subset=['screen_name'], keep='first')
    df["r_"+column] = df['r_screen_name'].map(lookup_df_col.set_index('screen_name')[column])

location = ['profile_location_lang', 'profile_location_en', 'profile_location_GPE', 'profile_location_country', 'profile_location_country_en']
for column in location:
    lookup_df_col = lookup_df.drop_duplicates(subset=['profile_location'], keep='first')
    df["r_"+column] = df['r_profile_location'].map(lookup_df_col.set_index('profile_location')[column])

def get_political(i):
    progress.update(1)
    try:
        result = scraper(i, False)._get_entity().label.description
    except:
        result = np.nan
    return result


lookup_political = df.drop_duplicates(subset=['r_screen_name'], keep='first')
progress = tqdm.tqdm(total=len(lookup_political), position=0, leave=True)
lookup_political['r_political'] = [get_political(i) for i in lookup_political['r_political']]

df['r_political'] = df['r_screen_name'].map(lookup_political.set_index('r_screen_name')['r_political'])


df.to_csv('result.csv', encoding='utf-8-sig')


# import pandas as pd
# df1 = {'col1': ["A", "A", "B", "C", "C", "F"], 'col2': [1,5,2,3,4,1]}
# df1 = pd.DataFrame(df1)
# df1 = df1.drop_duplicates(subset=['col2'], keep='first')
# df2 = {'colX': ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat"], 'colY': [2,3,5,4,1,1]}
# df2 = pd.DataFrame(df2)

# df2['colz'] = df2.colY.map(df1.set_index('col2').col1)
# print(df2)