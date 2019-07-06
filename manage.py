import pandas as pd
import os
import json

dataTwitter = pd.read_csv('not_sarcastic_data.csv')

#print current dataframe
print("Current DataFrame( size = ", len(dataTwitter),'):')
print(dataTwitter['in_reply'])
