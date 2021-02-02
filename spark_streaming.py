from pyspark import SparkContext
from pyspark.sql import *
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from elasticsearch import Elasticsearch
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf
from pyspark.sql import functions as F
from pyspark.sql.types import *
import json
import os
import functions as fn
from datetime import datetime
from ownelastic import to_elastic
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")
with open("hashtag.txt") as f:
    hashtag = f.read()

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--jars /home/prembamrung/Documents/Valdom/big_data_twitter/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar pyspark-shell"


def getSqlContextInstance(sparkContext):
    if "sqlContextSingletonInstance" not in globals():
        globals()["sqlContextSingletonInstance"] = SQLContext(sparkContext)
    return globals()["sqlContextSingletonInstance"]


def dosentiment(tweet):
    scores = dict([("pos", 0), ("neu", 0), ("neg", 0), ("compound", 0)])
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(tweet)
    for k in sorted(ss):
        scores[k] += ss[k]

    return json.dumps(scores)


def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        if rdd.count() == 0:
            raise Exception("Empty")
        sqlContext = getSqlContextInstance(rdd.context)
        df = sqlContext.read.json(rdd, multiLine=True)

        if df.count() == 0:
            raise Exception("Empty")
        udf_func = udf(lambda x: dosentiment(x), returnType=StringType())
        # print(df.head(5))
        df = df.withColumn("sentiment", lit(udf_func(df.text)))
        # print(df.take(10))
        results = df.toJSON().map(lambda j: json.loads(j)).collect()
        # print("Sentiment done")
        for result in results:
            result["created_at"] = fn.get_date(result["created_at"])
            result["cleaned_text"] = fn.clean(result["text"])
            result["sentiment"] = json.loads(result["sentiment"])
            polarity, tweet_sentiment = fn.get_sentiment(fn.get_tweet(result["text"]))
            result["sentiment_function"] = tweet_sentiment
            result["polarity"] = polarity
            result["source"] = fn.find_device(result["source"])
            result["user_age"] = fn.get_age(result["user"]["created_at"])
            # print("sentiment loaded")
        to_elastic(results, "tweet_" + hashtag + "_index", "doc")
        # print("Send to elastic done")
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":

    es = Elasticsearch(hosts=["localhost"], port=9200)
    # Create Spark Context to Connect Spark Cluster
    sc = SparkContext(appName="TwitterStreaming")

    # Set the Batch Interval is 10 sec of Streaming Context
    ssc = StreamingContext(sc, 6)

    # Create Kafka Stream to Consume Data Comes From Twitter Topic
    # localhost:2181 = Default Zookeeper Consumer Address

    kafkaStream = KafkaUtils.createStream(
        ssc, "localhost:2181", "spark-streaming", {"twitter_stream_" + hashtag: 1}
    )

    kafkaStream.map(lambda v: v[1]).foreachRDD(process)

    # Parse Twitter Data as json
    parsed = kafkaStream.map(lambda v: json.loads(v[1]))

    # Count the number of tweets per User
    author = parsed.map(
        lambda tweet: (tweet["user"]["screen_name"], 1)
    )  # .reduceByKey(lambda x, y: x + y)

    # Print the User tweet counts
    author.pprint()
    # parsed.foreachRDD(process)

    # Start Execution of Streams
    ssc.start()
    ssc.awaitTermination()