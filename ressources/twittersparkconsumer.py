#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:59:00 2020

@author: hustachethomas
"""


# import sys
from ownelastic import sth2elastic
from pyspark.sql import*
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf
from pyspark.sql.types import*
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime


import os

#os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /home/hustachethomas/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars ~/Documents/Valdom/big_data_twitter/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar pyspark-shell'


def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']


def dosentiment(tweet):
    scores = dict([('pos', 0), ('neu', 0), ('neg', 0), ('compound', 0)])
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(tweet)
    for k in sorted(ss):
        scores[k] += ss[k]

    return json.dumps(scores)


def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        if rdd.count() == 0:
            raise Exception('Empty')
        sqlContext = getSqlContextInstance(rdd.context)
        df = sqlContext.read.json(rdd)
        df = df.filter("text not like 'RT @%'")
        if df.count() == 0:
            raise Exception('Empty')
        udf_func = udf(lambda x: dosentiment(x), returnType=StringType())
        df = df.withColumn("sentiment", lit(udf_func(df.text)))
        print(df.take(10))
        results = df.toJSON().map(lambda j: json.loads(j)).collect()
        for result in results:
            result["date"] = datetime.strptime(
                result["date"], "%Y-%m-%d %H:%M:%S")
            result["sentiment"] = json.loads(result["sentiment"])
        sth2elastic(results, "tweets", "doc")
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreaming")
    # let it wait for 3 seconds to consume the next package of tweets
    ssc = StreamingContext(sc, 3)

    kafkaStream = KafkaUtils.createStream(
        ssc, "localhost:2181", "consumer-group", {"tweets": 1})
    lines = kafkaStream.map(lambda x: json.loads(x[1]))

    lines.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
