# The-BRI-on-Twitter

This repository stores the programming scripts applied to retrieve tweets and retweets related to the Belt and Road Initative by using Twitter APIs.
![Picture1](https://user-images.githubusercontent.com/64972156/170441406-6e6283ac-2cb6-4184-90cc-43c2ea146d07.png)


All scripts are categorized based on their purposes:

1.scraper.py: The scripts applied to download raw data (tweets) from Twitter

2.preprocessing.py: Extract valauble informaiton in the raw data. Also, there are some irrelevant tweets existed in the raw data due to the 
ambiguity of keywords applied in search, such as "seat belt and road safety" and the homonym of "silk road", which represents the online dark marketplace for selling drugs.
Therefore, the Irrelevance.py was applied to locate those potentailly irrelevant tweets.

3.NLP: This folder stores six files of python scripts for processing the textual information in the raw data.

3.1:language detection.py: Use FastText to detect the dominant language of texts in the columns: text, hashtag, bio, profile_location, political

3.2Translation.py: A script for executing neural machine translation by employing EasyNMT

3.3Sentiment Analysis.py: A script for running VADER, a lexicon-based sentiment analysis tool, on texts of tweets, in order to capture the sentimental polarity and intensity of tweets.

3.4Text_normalization.py: Using the natural language processing toolkit “NTLK”  to remove redundant information and retain the simplest form of words in tweets. 
Specifically, four steps were involved, including (1). translating emoticons into texts, (2). removing hyperlinks, usernames, punctuation, and modal verbs, 
(3). lemmatization, and (4). tokenization

3.5Named Entities Recognition.py: A script for interpretating The geographical locations of tweets based on the self-declared location fields in posters’ profiles. 
Since non-toponymic inputs, such as hyperlinks and emoticons may be found in location fields, NLTK was applied for identifying toponyms and eliminating irrelevant inputs.

3.6Geocoding.py: Employinh eocoding software Nominatim to extract the country names of recognized locations in order to classify different opinions around the BRI by nation

4.Retweet: This folder contains 
  
