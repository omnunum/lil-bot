# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 15:20:42 2014

@author: sunshine
"""
import pandas as pd
import re
from collections import defaultdict
import random as rnd

def generate_model_from_csv(path):
    tweets = pd.read_csv(path)['text']
    #doing some cleaning
    tweets = [re.sub(r'!+|\(|\"', '', re.sub(r'( +- +Lil B$)', '', tweet)) for tweet in tweets]
    model = defaultdict(list)
    
    for tweet in tweets:
        words = str(tweet).lower().strip().split(' ')
        for i, word in enumerate(words):
            if i < len(words) - 2:
                model[word].append(words[i+1])
    return model

def get_next_word(model, word):
    return rnd.choice(model[word])

def get_first_word(model):
    return rnd.choice(model.keys())
    
def build_tweet():
    model = generate_model_from_csv('tweets.csv')
    prev_word = get_first_word(model)
    tweet = prev_word + ' '
    signature = ' - Lil B'
    limit = (140 - len(signature)) - rnd.randrange(0, 40)
    
    while len(tweet) < limit:
        try:
            next_word = get_next_word(model, prev_word)
        except IndexError:
            break
        if len(tweet) + len(next_word + ' ') > limit:
            break
        else:
            tweet += next_word + ' '
        prev_word = next_word
    return tweet + signature
    
    