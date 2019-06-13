import json
import pandas as pd

sarcastic = pd.read_csv('twitter_sarcastic_data.csv')
print(sarcastic['text'])
