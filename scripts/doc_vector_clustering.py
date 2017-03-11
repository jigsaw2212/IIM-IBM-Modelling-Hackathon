import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import pandas as pd
import numpy as np
import joblib

db = MongoClient().finhack

model = gensim.models.Word2Vec.load(
    'word_vectors_with_lowercase_english_words_and_no_numbers_and_no_punct')

df = None

for i in range(4):
	all_docs = list()
    for doc in db['senti' + str(i)].find({}, {'dict_sent.tokens': True}):
        if len(doc['dict_sent']['tokens']) > 10:
            all_docs.append(doc)
        if df is None:
        	df = pd.DataFrame(all_docs)
        else:
        	df = pd.concat((df, pd.DataFrame(all_docs)))

df = df.apply(lambda x: ' '.join(x), axis=1)

tfidf = TfidfVectorizer()

tfidf.fit(df)

joblib.dump(tfidf, 'tfidf.pkl')
