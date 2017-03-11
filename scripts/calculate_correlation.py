from scipy.stats import pearsonr
from pymongo import MongoClient
import pandas as pd
import os

# db = MongoClient().finhack

# df = None


# for i in range(4):
#     sents = pd.DataFrame(list(
#         db['senti' + str(i)].find({'dict_sent.fls': True, 'dict_sent.sentiment.neu': {'$ne': 1}}, {'dict_sent.sentiment': True, 'doc_id': True})))
#     print sents.shape
#     sents = sents.apply(
#         lambda x: dict(x['dict_sent'].pop('sentiment'), id=int(str(x['doc_id'])[:6] + str(x['doc_id'])[-2:]), num=1), axis=1)
#     sents = sents.apply(lambda x: pd.Series(x))
#     sents = sents.groupby('id').sum()
#     print sents
#     if df is None:
#         df = sents
#     else:
#         df = df.add(sents, fill_value=0)

# df.to_pickle('sent_df.pkl')

df0 = pd.read_pickle('sent_df.pkl')

# CSV_PATH = "/home/ramparkash/Data/StockData/"
# FILES = os.listdir(CSV_PATH)
# FILES = [CSV_PATH + f for f in FILES]
# df2 = None

# for csv_file in FILES:
#     try:
#         df = pd.read_csv(csv_file).set_index('Date')
#     except:
#         continue
#     df = df.groupby(lambda x: int(x.split('-')[-1])).mean()
#     df['inc'] = df['Close Price'] - df['Close Price'].shift(1)
#     df.index = pd.Series(df.index.get_values()).apply(
#         lambda x: int(csv_file.split('/')[-1].rstrip('.csv') + str(x % 100)))
#     if df2 is None:
#         df2 = df
#     else:
#         df2 = pd.concat((df2, df))

# print df0.shape, df2.shape

# df2.to_pickle('price_df.pkl')

# df2 = pd.read_pickle('price_df.pkl')

df3 = df0.join(df2, how='inner')

df3 = df3.dropna()

df3['inc'] = df3['inc'].apply(lambda x: 1 if x > 0 else 0)

print df3.shape

print pearsonr(df3['neg']/df3['num'], df3['inc'])
