from pymongo import MongoClient
import numpy as np
import pandas as pd

db = MongoClient().finhack.textract_pdftotext
docs = pd.DataFrame(
    list(db.find({'text': {'$exists': True}}))).set_index('_id')
docs['len'] = docs['text'].apply(lambda x: len(x))
mean_len = docs['len'].mean()
median_len = docs['len'].median()
min_len = docs['len'].min()
max_len = docs['len'].max()
print mean_len, median_len, min_len, max_len
print docs['len'].sort_values().head(50)
