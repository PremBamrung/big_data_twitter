from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json
from textblob import TextBlob
from datetime import datetime
import datefinder
from langdetect import detect


es = Elasticsearch(hosts=['localhost'], port=9200)

def sentiment(tweet):
    polarity = tweet.sentiment.polarity
    tweet_sentiment = ""
    if polarity > 0:
        tweet_sentiment = 'positive'
    elif polarity < 0:
        tweet_sentiment = 'negative'
    elif polarity == 0:
        tweet_sentiment = 'neutral'
    return polarity,tweet_sentiment

def get_date(created_at):
    matches= datefinder.find_dates(created_at)
    date=str(next(matches,None))
    return date


def main():
    """
    main function initiates a kafka consumer, initialize the tweet database.
    Consumer consumes tweets from producer extracts features, cleanses the tweet text,
    calculates sentiments and loads the data into postgres database
    """

    # hashtag = input("Enter the hashtag : ")
    hashtag = "corona"

    # set-up a Kafka consumer
    consumer = KafkaConsumer("twitter_stream_" + hashtag,
                             auto_offset_reset='earliest')

    for msg in consumer:
        dict_data = json.loads(msg.value)
        tweet = TextBlob(dict_data["text"])
        # polarity = tweet.sentiment.polarity
        # tweet_sentiment = ""
        # if polarity > 0:
        #     tweet_sentiment = 'positive'
        # elif polarity < 0:
        #     tweet_sentiment = 'negative'
        # elif polarity == 0:
        #     tweet_sentiment = 'neutral'
        polarity,tweet_sentiment=sentiment(tweet)
        try:
            lang=detect(str(tweet))
        except:
            lang="unknown"
        # add text & sentiment to es
        es.index(
            index="tweet_es_" + hashtag + "_index",
            doc_type="test_doc",
            body={
                "author": dict_data["user"]["screen_name"],
                "created_at": dict_data["created_at"],
                "date": get_date(dict_data["created_at"]),        
                "message": dict_data["text"],
                "sentiment": tweet_sentiment,
                "lang":lang
            }
        )
        print(str(tweet))
        print('\n')


if __name__ == "__main__":
    main()
