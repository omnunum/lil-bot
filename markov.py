# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 15:20:42 2014

@author: sunshine
"""
import pandas as pd
import re
from collections import defaultdict
import random as rnd

def generate_model_from_csv(path, order):
    #grabs the text data from all the tweet entries
    tweets = pd.read_csv(path)['text']
    #doing some cleaning, removing some characters that throw everything off
    #also removes the variably spaced signature
    tweets = [re.sub(r'!+|\(|\"', '', re.sub(r'( +- +Lil B$)', '', tweet)) for tweet in tweets]
    
    model = defaultdict(list)
    for tweet in tweets:
        words = str(tweet).lower().strip().split(' ')
        for i, word in enumerate(words):
            if i < len(words) - order - 1:
                model[word].append(' '.join(words[i+1:i+1+order]).strip())
    return model

def get_next_word(model, word):
    return rnd.choice(model[word])

def get_first_word(model):
    return rnd.choice(model.keys())
    
def build_tweet():
    model = generate_model_from_csv('tweets.csv', 4)
    prev_word = get_first_word(model)
    tweet = prev_word + ' '
    signature = ' - Lil B'
    
    #makes sure our tweet fits the 140 limit, also includes an additional 
    #random limit to vary the length of the tweets
    limit = (140 - len(signature)) - rnd.randrange(0, 20)
    
    while len(tweet) < limit:
        try:
            #we use the last word of the returned chain entry of the specified order to lookup the next chain
            next_word = get_next_word(model, prev_word.split(' ')[-1])
        except IndexError:
            break
        if len(tweet) + len(next_word + ' ') > limit:
            break
        else:
            tweet += next_word + ' '
        prev_word = next_word
    #checks to see if the last word is in list of prepositions and pronouns
    words = tweet.split(' ')[:-2]
    with open('preps_and_pros.txt', 'r') as pnp:
        while words[-1] in pnp.read().split('\n'):
            words.pop()
    return ' '.join(words) + signature
    
    