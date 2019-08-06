import pandas as pd
import os
import json

df = pd.read_csv('sarcastic_data.csv')
sb = len(df)
print("tam before:" , sb)
df = df.drop_duplicates(['text'],keep='last')
print("Duplicated data Removed: ",sb - len(df))
#print new dataframe
print("Data Frame after this execution:")
print(df.tail())
#print current dataframe
# print("Current DataFrame( size = ", len(dataTwitter),'):')
# print(dataTwitter['in_reply'])
