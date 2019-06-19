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
if(os.path.isfile('twitter_sarcastic_data.csv')):
    print("CSV Already exists.\n reading...")
    dataTwitter = pd.read_csv('twitter_sarcastic_data.csv')
    dataTwitter = dataTwitter[['text', 'in_reply', 'is_sarcastic']]
else:
    print("CSV don't exists, new Data Frame created.\n")
    dataTwitter = pd.DataFrame(columns=['text','in_reply','is_sarcastic'])

#print current dataframe
print("Current DataFrame( size = ", len(dataTwitter),'):')
print(dataTwitter.tail(10))
old_size_df = len(dataTwitter)

#main code, reading tweets and get their text and the reply text if were a reply.
for tweet in tweepy.Cursor(api.search,q=["#sqn","#SQN","sqn","SQN"],count=10,tweet_mode="extended",result_type="recent",include_entities=True,lang="pt",locale='BR').items():
    print("\nTWEET:\n", tweet.full_text)
    if(tweet.in_reply_to_status_id != None):
        try:
            print("IN REPLY TO:\n", api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended").full_text)
            dataTwitter.loc[len(dataTwitter)] = [tweet.full_text, api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended").full_text, 1]    
           
        except:
            dataTwitter.loc[len(dataTwitter)] = [tweet.full_text, '', 1]    
    else:
        dataTwitter.loc[len(dataTwitter)] = [tweet.full_text, '', 1]    
    print('\n-------------------------------------------------------------------')

#print new dataframe
print("Data Frame after this execution:")       
print(dataTwitter.tail())
print("Added: ",len(dataTwitter) - old_size_df)

#write the df to csv file
dataTwitter.to_csv('twitter_sarcastic_data.csv', index=False)#
print("Sucessul Writing CSV to file")
