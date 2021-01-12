#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:05:44 2020

@author: hustachethomas
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json
from datetime import datetime
from datetime import timezone

access_token = "1338852601799041024-LMXAYz8JbzRbfmAVMSLuX8jocXqQfI"
access_token_secret = "cBwG5uYFWnaOnLiRN1UIkwdcQAtXawhsKiKC9u9C54cRS"
consumer_key = "1XVJBuHyrJFXHWHyYcoD1zLQN"
consumer_secret = "5HuwQhH3aESLL1yZYF5hXWH0tapA2xboG2xXGQI7ool68vVqoF"


def cleantweet(data):
    rawtweet = json.loads(data)
    tweet = {}

    tweet["user"] = rawtweet["user"]["screen_name"]

    tweet["date"] = datetime.strptime(rawtweet["created_at"], '%a %b %d %H:%M:%S %z %Y')\
        .replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
    if "extended_tweet" in rawtweet:
        tweet["text"] = rawtweet["extended_tweet"]["full_text"]
    else:
        tweet["text"] = rawtweet["text"]
    return json.dumps(tweet)


class StdOutListener(StreamListener):
    def on_data(self, data):
        #newdata = cleantweet(data)
        newdata = data
        producer.send("tweets", newdata)
        print(newdata)
        return True

    def on_error(self, status):
        print(status)


producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(
    0, 10, 1), value_serializer=lambda m: json.dumps(m).encode('ascii'))
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l, tweet_mode='extended')
stream.filter(track=["#trump"], languages=["en"])
# stream.filter(track="trump")
