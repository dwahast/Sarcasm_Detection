#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import tweepy
import pandas as pd
import json
import os

#Variables that contains the user credentials to access Twitter API
access_token = "243433303-wKdHFsVG2Lm5zpDY43L3phchSrTHAHTQejxsYj5S"
access_token_secret = "W3c7GbaU3S0wH2c5yXcniL3T8z42qADboaCR1WGDoblvh"
consumer_key = "gMChjJwVfA3FroAqExIqiUQfg"
consumer_secret = "flMX4koxYMpIbHvBhgX8iYpJ5MGxpfN1InEqs4RUfOUQK4ooYK"
limit = 10
find = ["#sqn","#SQN","#Sqn","sqn","SQN", "Sqn"]

class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
        self.limit = limit

    def on_data(self, data):
        global dataTwitter
        tweet = json.loads(data)
        tweet_text = ''
        reply_text = ''
        quoted_text = ''

        if('retweeted_status' in tweet):#ignoring RT (just is a tweet)

            return True

            # if('extended_tweet' in tweet['retweeted_status']):
            #     print('TWEET(RT EXT):', tweet['text'])
            #     tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
            # else:
            #     print('TWEET(RT):', tweet['text'])
            #     tweet_text = tweet['retweeted_status']['text']

        else:

            if(tweet['truncated'] != False):
                if(f in tweet['extended_tweet']['full_text'] for f in find):
                    print("TWEET(EXT):", tweet['extended_tweet']['full_text'])
                    tweet_text = tweet['extended_tweet']['full_text']
                else: return True
            else:
                if(f in tweet['text'] for f in find):
                    print('TWEET:', tweet['text'])
                    tweet_text = tweet['text']
                else:return True

            if('quoted_status' in tweet):
                if(tweet['quoted_status']['truncated'] == False):
                    print('QUOTED(Nor):', tweet['quoted_status']['text'])
                    quoted_text = tweet['quoted_status']['text']
                else:
                    print('QUOTED(EXT):', tweet['quoted_status']['extended_tweet']['full_text'])
                    quoted_text = tweet['quoted_status']['extended_tweet']['full_text']


            if(tweet['in_reply_to_status_id'] != None):
                print("\nIN REPLY TO:", api.get_status(tweet['in_reply_to_status_id'], tweet_mode="extended").full_text)
                reply_text = api.get_status(tweet['in_reply_to_status_id'], tweet_mode="extended").full_text

            dataTwitter.loc[len(dataTwitter)] = [tweet_text, reply_text, quoted_text, 1]

            self.num_tweets += 1

            print('----------------------- [ {} / {} ] -----------------------'.format(self.num_tweets,self.limit))

        if(self.num_tweets < self.limit):
            return True
        else:
            return False

    def on_error(self, status):
        print ("error", status)



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    l = StdOutListener()

    #if file exists
    if(os.path.isfile('sarcastic_data.csv')):
        print("CSV Already exists.\n reading...")
        dataTwitter = pd.read_csv('sarcastic_data.csv')
        dataTwitter = dataTwitter[['text', 'in_reply','quoted_text', 'is_sarcastic']]
    else:
        print("CSV don't exists, new Data Frame created.\n")
        dataTwitter = pd.DataFrame(columns=['text','in_reply','quoted_text','is_sarcastic'])

    #print current dataframe
    print("Current DataFrame( size = ", len(dataTwitter),'):')
    print(dataTwitter.tail(10),"\n")
    old_size_df = len(dataTwitter)

    stream = Stream(auth, l, tweet_mode="extended")

    print('----------------------- [ 0 / {} ] -----------------------'.format(limit))

    #This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=find, languages=['pt'])

    print("\nAdded: ",len(dataTwitter) - old_size_df)

    #drop duplicated rows
    lb = len(dataTwitter)
    dataTwitter = dataTwitter.drop_duplicates(['text'],keep='last')
    print("Duplicated data Removed: ",lb - len(dataTwitter))
    print("\nRelevant Added: ",len(dataTwitter) - old_size_df)

    #print new dataframe
    print("Data Frame after this execution:")
    print(dataTwitter.tail())

    #write the df to csv file
    dataTwitter.to_csv('sarcastic_data.csv', index=False)#
    print("Sucessul Writing CSV to file")
