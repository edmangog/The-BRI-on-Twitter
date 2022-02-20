import pandas as pd
import re

df = pd.read_csv(r'result.csv',index_col=0, header=0, encoding='utf-8-sig')
stop_punctuation = "\"[',]"


def remove_punctuation(x):
    x = str(x)
    return x.translate(x.maketrans('', '', stop_punctuation))


##1.links/hashtag/cashtag:
df['links'] = [remove_punctuation(x) for x in df['links'].fillna('')]
df['hashtag'] = [remove_punctuation(x) for x in df['hashtag'].fillna('')]
df['cashtag'] = [remove_punctuation(x) for x in df['cashtag'].fillna('')]

##2.Media column
df.insert(10, 'image_url', '')
df.insert(11, 'video_url', '')
df.insert(12, 'GIF_url', '')
df['image_url'] = [x if "Photo(previewUrl" in x else '' for x in df['media'].fillna('')]
df['image_url'] = [re.findall('fullUrl=(.*?)\)', x) if x else '' for x in df['image_url'].fillna('')]
df['image_url'] = [remove_punctuation(x) for x in df['image_url'].fillna(' ')]

df['GIF_url'] = [x if "Gif(thumbnail" in x else '' for x in df['media'].fillna('')]
df['GIF_url'] = [re.findall(', url=(.*?), ', x) if x else '' for x in df['GIF_url'].fillna('')]
df['GIF_url'] = [remove_punctuation(x) for x in df['GIF_url'].fillna(' ')]

df['video_url'] = [x if "Video(thumbnail" in x else '' for x in df['media'].fillna('')]
highest_res = [re.findall('bitrate=(.*?)\)', x) if x else '' for x in df['video_url'].fillna('')]
highest_res = [ [y for y in x if y not in ('None')] for x in highest_res] #nested, Eliminated 'None'
highest_res = [str(max([int(i) for i in x])) if x else '' for x in highest_res]
df['video_url'] = [re.search("url='((?:(?!url).)*?)', bitrate="+y, x).group(1) if x else '' if y else '' for x,y in zip(df['video_url'].fillna(''), highest_res)]

##3, extract reply_to_user screen_name
df['reply_to_user'] = [re.search('.com/(.*)',x).group(1) if x else '' for x in df['reply_to_user'].fillna('')]

##4. extract mentioned users
df['mentioned_users'] = [re.findall('username=(.*?), id=',x) if x else '' for x in df['mentioned_users'].fillna('')]
df['mentioned_users'] = [remove_punctuation(x) for x in df['mentioned_users'].fillna('')]

##5.divide coordinates into two columns:
df.insert(23, 'tweet_long', '')
df.insert(24, 'tweet_lat', '')
df['tweet_long'] = [re.search("longitude=(.*?), ", x).group(1) if x else '' for x in df['coordinates'].fillna('')]
df['tweet_lat'] = [re.search("latitude=(.*?)\)", x).group(1) if x else '' for x in df['coordinates'].fillna('')]

##6.divide place into two columns: 
df.insert(26, 'tweet_location', '')
df.insert(27, 'tweet_location_type', '')
df.insert(28, 'tweet_location_country', '')
df['tweet_location'] = [re.search("fullName=(.*?), ", x).group(1) if x else '' for x in df['place'].fillna('')]
df['tweet_location'] = [remove_punctuation(x) for x in df['tweet_location'].fillna(' ')]
df['tweet_location_type'] = [re.search("type=(.*?), ", x).group(1) if x else '' for x in df['place'].fillna('')]
df['tweet_location_type'] = [remove_punctuation(x) for x in df['tweet_location_type'].fillna(' ')]
df['tweet_location_country'] = [re.search("country=(.*?), ", x).group(1) if x else '' for x in df['place'].fillna('')]
df['tweet_location_country'] = [remove_punctuation(x) for x in df['tweet_location_country'].fillna(' ')]

##7.User label
df.insert(34, 'political', '')
df['political'] = [re.search("description=(.*?), url", x).group(1) if x else '' for x in df['label'].fillna('')]
df['political'] = [remove_punctuation(x) for x in df['political'].fillna(' ')]

df.to_csv('result.csv', encoding='utf-8-sig')