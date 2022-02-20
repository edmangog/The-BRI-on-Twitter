import tweepy
import json
from rich import print
import pandas as pd
import re
import time
import random
import tqdm

auth = [tweepy.AppAuthHandler('', ''),
        tweepy.AppAuthHandler('', ''),
        tweepy.AppAuthHandler('', ''),
        tweepy.AppAuthHandler('', ''),
        tweepy.AppAuthHandler('', ''),
        ]
API = tweepy.API(auth[1])
# rate_remain = API.rate_limit_status()['resources']['statuses']['/statuses/retweets/:id']['remaining']

df = pd.read_csv(r'result.csv', index_col=0, header=0, encoding='utf-8-sig')

def retweet(url):
    id = re.search("([^\/]+$)", url).group(1)
    author = re.search("twitter.com[\/](.*?)[\/]status", url).group(1)
    res = API.get_retweets(id, count='1000')
    for i in res:
        res_item  = json.loads(json.dumps(i._json))
        dict = {
            'tweet_url': url,
            'screen_name': author,
            'r_timestamp':res_item.get('created_at'),
            'r_screen_name': res_item.get('user').get('screen_name'),
            'r_username': res_item.get('user').get('name'),
            'r_user_id': res_item.get('user').get('id'),
            'r_bio':res_item.get('user').get('description'),
            'r_verified':res_item.get('user').get('verified'),
            'r_date_joined':res_item.get('user').get('created_at'),
            'r_profile_url':res_item.get('user').get('url'),
            'r_profile_image':res_item.get('user').get('profile_image_url_https'),
            'r_profile_banner': res_item.get('user').get('profile_banner_url'),
            'r_profile_location':res_item.get('user').get('location'),
            'r_protected':res_item.get('user').get('protected'),
            'r_num_tweets': res_item.get('user').get('statuses_count'),
            'r_media_count': res_item.get('user').get('media_count'),
            'r_followers':res_item.get('user').get('followers_count'),
            'r_following':res_item.get('user').get('friends_count'),
        }
        rt_list.append(dict)
        # scrape columns:: label
        # add columns: bio_lang, bio_en, political, political_lang, political_en, profile_location_lang, profile_location_en


df = df.loc[df['retweets'] != 0]
t_list = ['https://twitter.com/SAISHopkins/status/1312409578668138496']
# t_list = df['tweet_url']
rt_list = []

progress = tqdm.tqdm(total=len(t_list), position=0, leave=True)
for url in t_list:

    try:
        retweet(url)
    except tweepy.errors.TooManyRequests: #IF limited, Then switch key
        try:
            available_token = [x for x in auth if
                            tweepy.API(x).rate_limit_status()['resources']['statuses']['/statuses/retweets/:id']['remaining'] > 0]
            if available_token:
                API = tweepy.API(random.choice(available_token))
                retweet(id)
            else:
                time.sleep(920)
                retweet(id)
        except:
            pass
    except:  # Rest of the exceptions, e.g. User not found/Private
        pass
    progress.update(1)

df1 = pd.DataFrame(rt_list)
df1.to_csv('result_API1.csv', encoding='utf-8-sig')