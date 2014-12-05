#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd

#Twitter API credentials
consumer_key = "BB3TrvSEOM9jTC6nqCsTBRz9O"
consumer_secret = "2f6miJPcxmUEbwL6XX93UK9o27Sysq49tqYOBiv1SlPIBCcKd6"
access_key = ""
access_secret = ""

def init_tweepy():
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)
     
def download_new_tweets(screen_name):
    api = init_tweepy()
    api_tweets_raw = pd.DataFrame([[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in api.user_timeline(screen_name = screen_name,count=200)], columns=['id', 'created_at', 'text'])
    api_tweets_cleaned = api_tweets_raw[~api_tweets_raw['text'].str.contains('@|http')]
    api_tweets_cleaned = api_tweets_cleaned.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, basestring) else x)
    csv_tweets = pd.read_csv('tweets.csv')
    comp = pd.concat([csv_tweets, api_tweets_cleaned], axis=0, ignore_index=True).drop_duplicates(subset='text', take_last=True).sort('id', ascending=False)
    comp.to_csv('tweets.csv', index=False)
    return comp
    
if __name__ == '__main__':
    #pass in the username of the account you want to download
    #download_new_tweets("lilbthebasedgod")
    pass