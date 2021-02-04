from pyspark import SparkContext,SparkConf
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
from ownelastic import to_elastic,readLinedJSON,createIndex
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import numpy as np

nltk.download("vader_lexicon")
with open("hashtag.txt") as f:
    hashtag = f.read()



import requests





os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--jars ~/server/spark-2.4.7-bin-hadoop2.7/jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar pyspark-shell"


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

def send_top_trends(filename):
    #trends = readLinedJSON(filename)
    
    with open(filename) as f:
        trends = json.load(f)  
        print('trends[0]',trends[0])
        print('\n')
        print('trends',trends)
    to_elastic(trends[0], "tweet_trends_index", "doc")
    return True
    
def find_top_topics(n=3,file_name = "twitter_top_trends.json"):
    with open(file_name) as f:
        data = json.load(f)
    max_volumes = []
    for ind,value in enumerate(data[0]['trends']):
                  
        max_volumes+=[value['tweet_volume']]
    indices_sorted = np.argsort(max_volumes)
    top_topics=[]
    for i in (indices_sorted[::-1])[:n]:
        top_topics+=[data[0]['trends'][i]['name']]
    return top_topics


def process(time, rdd):
    
    print('enter process function')
    print("========= %s =========" % str(time))
    try:
        if rdd.count() == 0:
            raise Exception("rdd.count == 0 , Empty")
        sqlContext = getSqlContextInstance(rdd.context)
        df = sqlContext.read.json(rdd, multiLine=True)

        if df.count() == 0:
            raise Exception("df.count ==0 , Empty")
        udf_func = udf(lambda x: dosentiment(x), returnType=StringType())
        #print(df.head(5))
        df = df.withColumn("sentiment", lit(udf_func(df.text)))
        #print(df.take(10))
        results = df.toJSON().map(lambda j: json.loads(j)).collect()
        print("Sentiment done")
        for result in results:
            
            result["created_at"] = fn.get_date(result["created_at"])
            result["cleaned_text"] = fn.clean(result["text"])
            result["sentiment"] = json.loads(result["sentiment"])
            polarity, tweet_sentiment = fn.get_sentiment(fn.get_tweet(result["text"]))
            result["sentiment_function"] = tweet_sentiment
            result["polarity"] = polarity
            result["source"] = fn.find_device(result["source"])
            result["user_age"] = fn.get_age(result["user"]["created_at"])
            for topic in top_topics:
                
                if topic in result['text']:
                    
                    result['topic'] = topic
                    print(result['topic'])
                
            
            print("sentiment loaded")
        to_elastic(results, "main_index", "doc")
        
        print('sent to elastic')
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    
    

    
    es = Elasticsearch(hosts=["localhost"], port=9200)
    os.system('curl -XDELETE localhost:9200/main_index')
    
    
    createIndex('main_index')
    
    headers = {
    "Content-Type": "application/json",
    }
    
    resp = requests.put(
        'http://localhost:9200/main_index/_settings',
        headers=headers,
        data='{"index": {"mapping": {"total_fields": {"limit": "2000"}}}}',
    )
    
    print(f"\nHTTP code: {resp.status_code} -- response: {resp}\n")
    print(f"Response text\n{resp.text}")
    
    # Create Spark Context to Connect Spark Cluster
    conf = SparkConf()
    conf.setAppName('TwitterStreaming').set("spark.io.compression.codec", "snappy")
    sc = SparkContext(conf=conf)

    # Set the Batch Interval is 10 sec of Streaming Context
    ssc = StreamingContext(sc, 10)

    # Create Kafka Stream to Consume Data Comes From Twitter Topic
    # localhost:2181 = Default Zookeeper Consumer Address

    kafkaStream = KafkaUtils.createStream(
        ssc, "localhost:2181", "spark-streaming", {"twitter_fullstream": 1}
    )

    
    
    # os.system('curl -XDELETE localhost:9200/tweet_vaccine_index')
    
    
    # print('indexes deleted from elastic')
    # send_top_trends('twitter_top_trends.json')
    # print('trends sent to elastic')
    
    top_topics = find_top_topics()
    print(top_topics)
    kafkaStream.map(lambda v: v[1]).foreachRDD(process)
    

    print('process done')
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