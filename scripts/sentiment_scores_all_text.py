from multiprocessing import Pool
from pymongo import MongoClient
import functools
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

db = MongoClient(connect=False).finhack
analyzer = SentimentIntensityAnalyzer()


def f(i, (j, doc)):
    # print(i, j)
    for k in ('raw_sent', 'dict_sent'):
        text = doc.pop(k)
        doc[k] = {
            'text': text, 'sentiment': analyzer.polarity_scores(text)}
    db['senti' +
        str(i)].update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)


if __name__ == '__main__':
    pool = Pool(10)
    for i in range(4):
        sent_db = db['sent' + str(i)]
        pool.map(functools.partial(f, i), ((j, doc)
                                           for j, doc in enumerate(sent_db.find())))
        # functools.partial(f, i)(sent_db.find_one())
