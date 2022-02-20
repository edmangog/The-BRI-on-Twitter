# RUN with PYTHON 3.8+
# SNSCRAPE VERSION: 0.3.5.dev138+ga6b6f3f (commit:a6b6f3f)
import snscrape.modules.twitter as SMT
import pandas as pd

query = SMT.TwitterSearchScraper(
    '"belt and road" OR "beltandroad" OR "one belt one road" OR "onebeltoneroad" OR "new silk road" OR "newsilkroad" OR "silk road economic belt" OR "silkroadeconomicbelt" OR "maritime silk road" OR "maritimesilkroad" since:2013-09-01 until:2020-09-01').get_items()

tweet_detail = []

for i, tweet in enumerate(query):
    print(i)
    tweet_detail.append({
        # snscrape.base.Item
                        "screen_name": tweet.user.username,
                        "username":  tweet.user.displayname,
                        "tweet_url": tweet.url,
                        "timestamp": tweet.date,
                        "tweet_id": tweet.id,
                        "text": tweet.content,
                        "text_lang": tweet.lang,
                        "links": tweet.outlinks,
                        "hashtag": tweet.hashtags,
                        "cashtag": tweet.cashtags,
                        "media": tweet.media,
                        "likes": tweet.likeCount,
                        "retweets": tweet.retweetCount,
                        "replies": tweet.replyCount,
                        "reply_to_user": tweet.inReplyToUser,
                        "reply_to_user_tweet": tweet.inReplyToTweetId,
                        "mentioned_users": tweet.mentionedUsers,
                        "quoted_tweet": tweet.quotedTweet,
                        "quoted_by_count": tweet.quoteCount,
                        # "original_tweet": tweet.retweetedTweet,
                        "coordinates": tweet.coordinates,
                        "place": tweet.place,
                        "tweet_source": tweet.sourceLabel,
		# snscrape.base.Entity
                        "user_id": tweet.user.id,
                        "bio": tweet.user.description,
                        "verified": tweet.user.verified,
                        "label": tweet.user.label,
                        "date_joined": tweet.user.created,
                        "profile_url": tweet.user.linkUrl,
                        "profile_image": tweet.user.profileImageUrl,
                        "profile_banner": tweet.user.profileBannerUrl,
                        "profile_location": tweet.user.location,
                        # "protected": tweet.user.protected,
                        "num_tweets": tweet.user.statusesCount,
                        "media_count": tweet.user.mediaCount,
                        "followers": tweet.user.followersCount,
                        "following": tweet.user.friendsCount,
                        })

df = pd.DataFrame(tweet_detail)
df.to_csv('result.csv', encoding='utf-8-sig')
