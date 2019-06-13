#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import pandas as pd
import json
import os

#Variables that contains the user credentials to access Twitter API
access_token = "243433303-wKdHFsVG2Lm5zpDY43L3phchSrTHAHTQejxsYj5S"
access_token_secret = "W3c7GbaU3S0wH2c5yXcniL3T8z42qADboaCR1WGDoblvh"
consumer_key = "gMChjJwVfA3FroAqExIqiUQfg"
consumer_secret = "flMX4koxYMpIbHvBhgX8iYpJ5MGxpfN1InEqs4RUfOUQK4ooYK"

#if file exists open the file and read for append new rows
if(os.path.isfile('twitter_sarcastic_data.csv')):
    dataTwitter = pd.read_csv('twitter_sarcastic_data.csv')
    dataTwitter = dataTwitter[['text', 'is_sarcastic']]
else:
    dataTwitter = pd.DataFrame(columns=['text','is_sarcastic'])

print(dataTwitter.tail(10))
print('size of DataFrame:',len(dataTwitter))

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0

    def on_data(self, data):
        global dataTwitter
        tweet = json.loads(data)
        if('extended_tweet' in tweet):
            print("Extended Tweet:")
            print (tweet['extended_tweet']['full_text'])
            tweet = [(tweet['extended_tweet']['full_text'])]
        else:
            print("Normal Tweet")
            print (tweet['text'])
            tweet = [(tweet['text'])]
        #print(type(tweet))
        self.num_tweets += 1
        dataTwitter.loc[len(dataTwitter)] = [''.join(tweet), 1]
        #print(dataTwitter.sample())

        if(self.num_tweets <= 3):
            print('Success: ', self.num_tweets)
            return True
        else:
            return False

    def on_error(self, status):
        print ("error", status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    stream = Stream(auth, l, tweet_mode="extended")

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['SQN','sqn', '#SQN','#sqn'], languages=['pt'])
    #searched_tweets = api.search(q='#sqn', lang='pt', locale='BR', count=500, tweet_mode="extended")

    #write the df to csv file
    dataTwitter.to_csv('twitter_sarcastic_data.csv', index=False)#

    print(dataTwitter.tail())

    #tweets_data = []

    #for i, tweet in enumerate(searched_tweets):
    #    tweets_data.append(tweet._json)
    #    print("Tweet", i,": \n")
    #    print(tweets_data[i]['full_text'])
    #    print("\n")

    #print(tweets_data)
