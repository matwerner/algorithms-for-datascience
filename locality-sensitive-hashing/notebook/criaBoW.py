import pandas as pd
from utils import *

df = pd.read_json('../datasets/development.json', orient='records')
df.sample(10).head(10)

stopwords = list(get_stopwords())

stemmer= get_stemmer()

tokenfy = lambda x : tokenizer(x, stopwords= stopwords, stemmer=stemmer)
df['token_title'] = df['title'].transform(tokenfy)
df.sample(10).head(10)

df['token_description'] = df['description'].transform(tokenfy)

word2idx={}

df = data2idx(df, word2idx)

bow = data2bow(df, word2idx)
