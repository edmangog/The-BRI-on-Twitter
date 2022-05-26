import tweepy
import pandas as pd
from rich import print
import json

API = tweepy.Client(
    bearer_token='',
    return_type=dict
)

def get_tweet(query):
    return API.search_all_tweets(
        query=query,
        start_time='2021-11-18T10:00:00Z',
        end_time='2021-11-19T00:00:00Z',
        expansions=[
            'author_id',
            'referenced_tweets.id',
            'referenced_tweets.id.author_id',
            'entities.mentions.username',
            'attachments.poll_ids',
            'attachments.media_keys',
            'in_reply_to_user_id',
            'geo.place_id'
        ],
        media_fields=[
            'duration_ms',
            'height',
            'media_key',
            'preview_image_url',
            'type',
            'url',
            'width',
            'public_metrics',
            'alt_text'
        ],
        place_fields=[
            'contained_within',
            'country',
            'country_code',
            'full_name',
            'geo',
            'id',
            'name',
            'place_type'
        ],
        poll_fields=[
            'duration_minutes',
            'end_datetime',
            'id',
            'options',
            'voting_status',
        ],
        tweet_fields=[
            'attachments',
            'author_id',
            'context_annotations',
            'conversation_id',
            'created_at',
            'entities',
            'geo',
            'id',
            'in_reply_to_user_id',
            'lang',
            # 'non_public_metrics',
            # 'organic_metrics',
            'possibly_sensitive',
            # 'promoted_metrics',
            'public_metrics',
            'referenced_tweets',
            'reply_settings',
            'source',
            'text',
            'withheld'],
        user_fields=[
            'created_at',
            'description',
            'entities',
            'id',
            'location',
            'name',
            'pinned_tweet_id',
            'profile_image_url',
            'protected',
            'public_metrics',
            'url',
            'username',
            'verified',
            'withheld'
        ],
    )

result = get_tweet("belt and road OR beltandroad OR one belt one road OR onebeltoneroad OR new silk road OR newsilkroad OR silk road economic belt OR silkroadeconomicbelt OR maritime silk road OR maritimesilkroad")
df = pd.json_normalize(result)
df.to_csv('test.csv', encoding='utf-8-sig')

