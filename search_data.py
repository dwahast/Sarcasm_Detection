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

#This handles Twitter authetification and the connection to Twitter Streaming API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

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
print(dataTwitter.tail(10))
old_size_df = len(dataTwitter)
limit = 2000
num_tweets = 0
#main code, reading tweets and get their text and the reply text if were a reply.
print('----------------------- [ {} / {} ] -----------------------'.format(num_tweets,limit))
find = ["#sqn","#SQN","#Sqn","sqn","SQN", "Sqn"]
while num_tweets < limit:
    for tweet in tweepy.Cursor(api.search,
                                q=find,
                                count=100,
                                tweet_mode="extended",
                                result_type="mixed",
                                include_entities=True,
                                lang="pt",
                                locale='BR').items(limit):
        tweet_text,reply_text,quoted_text = '','',''
        tweet = tweet._json
        #print(tweet)
        if(not 'retweeted_status' in tweet):#ignoring RT (just is a tweet)
            if(f in tweet['full_text'] for f in find ):
                print("TWEET(EXT):", tweet['full_text'])
                tweet_text = tweet['full_text']

                if('quoted_status' in tweet):
                    #print(tweet)
                    print('QUOTED(Nor):', tweet['quoted_status']['full_text'])
                    quoted_text = tweet['quoted_status']['full_text']

                if(tweet['in_reply_to_status_id'] != None):
                    try:
                        print("\nIN REPLY TO:", api.get_status(tweet['in_reply_to_status_id'], tweet_mode="extended").full_text)
                        reply_text = api.get_status(tweet['in_reply_to_status_id'], tweet_mode="extended").full_text
                    except:
                        pass
                dataTwitter.loc[len(dataTwitter)] = [tweet_text, reply_text, quoted_text, 1]
                num_tweets += 1
                print('----------------------- [ {} / {} ] -----------------------'.format(num_tweets,limit))

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
