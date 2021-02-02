from kafka import KafkaProducer
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import geocoder

access_token = "1338852601799041024-LMXAYz8JbzRbfmAVMSLuX8jocXqQfI"
access_secret = "cBwG5uYFWnaOnLiRN1UIkwdcQAtXawhsKiKC9u9C54cRS"
consumer_key = "1XVJBuHyrJFXHWHyYcoD1zLQN"
consumer_secret = "5HuwQhH3aESLL1yZYF5hXWH0tapA2xboG2xXGQI7ool68vVqoF"


# hashtag = input("Enter the hashtag : ")
with open("hashtag.txt") as f:
    hashtag = f.read()


# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def top_trends(place = 'France'):
               
    # Trends for Specific Country
    g = geocoder.osm(place) # getting object that has location's latitude and longitude

    closest_loc = api.trends_closest(g.lat, g.lng)
    print(closest_loc[0])
    trends = api.trends_place(closest_loc[0]['woeid'])
    # writing a JSON file that has the latest trends for that location
    with open("twitter_"+place+"_trend.json","w") as wp:
        wp.write(json.dumps(trends, indent=1))
    
    return True


# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    # Get Producer that has topic name is Twitter
    # self.producer = self.client.topics[bytes("twitter")].get_producer()

    def on_data(self, data):
        # Producer produces data for consumer
        # Data comes from Twitter
        self.producer.send("twitter_stream_" + hashtag, data.encode("utf-8"))
        print(data)
        return True

    def on_error(self, status):
        print(status)
        return True


top_trends()
# # Twitter Stream Config
# twitter_stream = Stream(auth, KafkaPushListener())

# hashStr = "#" + hashtag

# # Produce Data that has trump hashtag (Tweets)
# twitter_stream.filter(track=[hashStr])
