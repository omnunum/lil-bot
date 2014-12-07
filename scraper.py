#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import pandas as pd
import markov
import os, sys

#Twitter API credentials
consumer_key = "BB3TrvSEOM9jTC6nqCsTBRz9O"
consumer_secret = "2f6miJPcxmUEbwL6XX93UK9o27Sysq49tqYOBiv1SlPIBCcKd6"
access_key = "577497821-TG8PZ83EKMJdBxad0FfuiFl7DgGtkZOgVJuWmF5J"
access_secret = "7V9UDzWh2QjTxvwmTvg6K11SL8MuxhEPX3GHYdntj4vPM"


def init_tweepy():
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)
     
def download_new_tweets(api, screen_name):
    #grabs the relevant information from the most recent 200 tweets
    api_tweets_raw = pd.DataFrame([[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in api.user_timeline(screen_name = screen_name,count=200)], columns=['id', 'created_at', 'text'])
    #removes tweets containing links and retweets/DMs
    api_tweets_cleaned = api_tweets_raw[~api_tweets_raw['text'].str.contains('@|http')]
    #filters out newlines from the tweets' text
    api_tweets_cleaned = api_tweets_cleaned.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, basestring) else x)
    #loads previously stored tweets
    csv_tweets = pd.read_csv(os.path.realpath('tweets.csv'))
    #concats the previously stored tweets with the newly downloaded tweets
    #removes duplicates and sorts based on tweed id (age)
    comp = pd.concat([csv_tweets, api_tweets_cleaned], axis=0, ignore_index=True).drop_duplicates(subset='text', take_last=True).sort('id', ascending=False)
    #saves new table to disk
    comp.to_csv(os.path.realpath('tweets.csv'), index=False)
    return comp
    
def send_tweet(api, tweet):
    api.update_status(tweet)
    
if __name__ == '__main__':
    api = init_tweepy()
    if len(sys.argv) > 1:
        download_new_tweets(api, sys.argv[1])
    else:
        download_new_tweets(api, 'lilbthebasedgod')
    send_tweet(api, markov.build_tweet())
    pass