# The-BRI-on-Twitter: More than one million Belt and Road Initaitive (re)tweets with annotations of languague, sentiment, and geopolitical entities

This repository stores the programming scripts applied to retrieve tweets and retweets related to the Belt and Road Initiative
![Picture1](https://user-images.githubusercontent.com/64972156/195039728-a144ea8b-96fc-4d00-aa63-67cb9699ba52.png)


All scripts are categorized based on their purposes:

1.scraper.py: The scripts applied to download raw data (tweets) from Twitter

2.preprocessing.py: Extract valuable information in the raw data. Also, there are some irrelevant tweets existed in the raw data due to the 
ambiguity of keywords applied in search, such as "seat belt and road safety" and the homonym of "silk road", which represents the online dark marketplace for selling drugs.
Therefore, the Irrelevance.py was applied to locate those potentially irrelevant tweets.

3.NLP: This folder stores six files of python scripts for processing the textual information in the raw data.
<!-- TABLE_GENERATE_START -->

| Script  | Description |
| ------------- | ------------- |
| 3.1 Language detection.py | Use FastText to detect the dominant language of texts in the columns: text, hashtag, bio, rofile_location, political identity |
| 3.2 Translation.py | A script for executing neural machine translation by employing EasyNMT  |
| 3.3 Sentiment Analysis.py | A script for running VADER, a lexicon-based sentiment analysis tool, on texts of tweets,in order to capture the sentimental polarity and ntensity of tweets.  |
| 3.4 Text_normalization.py | Using the natural language processing toolkit “NTLK”  to remove redundant information and retain the simplest form of words in tweets. Specifically, four steps were involved, including (1). translating emoticons into texts, (2). removing hyperlinks, usernames, punctuation, and modal verbs, (3). lemmatization, and (4). tokenization  |
| 3.5 Named Entities Recognition.py | A script for interpreting the geographical locations of tweets based on the self-declared location fields in posters’ profiles. Since non-toponymic inputs, such as hyperlinks and emoticons may be found in location fields, NLTK was applied for identifying toponyms and eliminating irrelevant inputs.  |
| 3.6 Geocoding.py | A script for employing Geocoding software Nominatim to extract the country names of recognized locations in order to classify different opinions around the BRI by nation  |

<!-- TABLE_GENERATE_END -->
4.1GetRetweets.py: The scripts for retrieving retweets by using Twitter APIs

# Download
Dataset: https://figshare.com/articles/dataset/The_Belt_and_Road_Initiative_on_Twitter_An_Annotated_Dataset/18623522

# Tweets hydration
To fetches full tweet content, such as the URLs of tweets and user handles, variables of unique identifiers of Twitter users and tweets contained in the dataset : “user_id” and “tweet_id” can be used to hydrate tweets by using Twitter APIs.
