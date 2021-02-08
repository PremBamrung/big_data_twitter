from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json
import functions as fn
import os

es = Elasticsearch(hosts=["localhost"], port=9200)


def main():
    """
    main function initiates a kafka consumer, initialize the tweet database.
    Consumer consumes tweets from producer extracts features, cleanses the tweet text,
    calculates sentiments and loads the data into postgres database
    """

    # hashtag = input("Enter the hashtag : ")
    # hashtag = "corona"
    with open("hashtag.txt") as f:
        hashtag = f.read()

    # set-up a Kafka consumer
    consumer = KafkaConsumer("twitter_stream_" + hashtag, auto_offset_reset="earliest")
    os.system("curl -XDELETE localhost:9200/main_index")

    for msg in consumer:
        dict_data = json.loads(msg.value)
        tweet = fn.get_tweet(dict_data["text"])
        polarity, tweet_sentiment = fn.get_sentiment(tweet)
        lang = fn.detect_lang(tweet)

        # add text & sentiment to es
        es.index(
            index="main_index",
            doc_type="test_doc",
            body={
                "author": dict_data["user"]["screen_name"],
                "author_followers": dict_data["user"]["followers_count"],
                "author_statues": dict_data["user"]["statuses_count"],
                "author_verified": dict_data["user"]["verified"],
                "author_account_age": fn.get_age(dict_data["user"]["created_at"]),
                "created_at": dict_data["created_at"],
                "@timestamp": fn.get_date(dict_data["created_at"], to_string=False),
                "message": dict_data["text"],
                "cleaned_text": fn.clean(dict_data["text"]),
                "sentiment_function": tweet_sentiment,
                "polarity": polarity,
                "lang": lang,
                "source": fn.find_device(dict_data["source"]),
            },
        )
        print(str(tweet))
        print("\n")


if __name__ == "__main__":
    main()


"""
with open("hastag.txt") as f :
    hashtag=f.read()

consumer = KafkaConsumer("twitter_stream_" + hashtag,
                            auto_offset_reset='earliest')


for msg in consumer:
    data=json.loads(msg.value)
    print(data['text'])
    print(" ")


dict_keys(['created_at', 'id', 'id_str', 'text', 'source', 'truncated', 'in_reply_to_status_id',
           'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str',
           'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors',
           'retweeted_status', 'quoted_status_id', 'quoted_status_id_str', 'quoted_status',
           'quoted_status_permalink', 'is_quote_status', 'quote_count', 'reply_count',
           'retweet_count', 'favorite_count', 'entities', 'favorited', 'retweeted', 'filter_level',
           'lang', 'timestamp_ms'])
"""