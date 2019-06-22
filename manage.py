import pandas as pd
import os
import json
# if(os.path.isfile('test.csv')):
#     print("CSV Already exists.\n reading...")
#     dataTwitter = pd.read_csv('test.csv')
#     dataTwitter = dataTwitter[['text', 'in_reply', 'is_sarcastic']]
# else:
#     print("CSV don't exists, new Data Frame created.\n")
#     dataTwitter = pd.DataFrame(columns=['text','in_reply','is_sarcastic'])
#
# #print current dataframe
# print("Current DataFrame( size = ", len(dataTwitter),'):')
# print(dataTwitter)

with open('data.json', 'r') as f:
    distros_dict = json.load(f)

print(distros_dict['retweeted_status']['extended_tweet']['full_text'])
