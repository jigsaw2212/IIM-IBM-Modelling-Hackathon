from multiprocessing import Pool
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize, word_tokenize
import functools

db = MongoClient(connect=False).finhack
fls_words = set(["will", "should", "can", "could", "may", "might", "expect", "anticipate",
                 "believe", "plan", "hope", "intend", "seek", "project", "forecast", "objective", "goal"])


def f(i, doc):
    if len(set(doc['dict_sent']['tokens']) & fls_words) > 0:
        db['senti' +
            str(i)].update_one({'_id': doc['_id']}, {'$set': {'dict_sent.fls': True}})


if __name__ == '__main__':
    pool = Pool(10)
    for i in range(4):
        sent_db = db['senti' + str(i)]
        pool.map(functools.partial(f, i), sent_db.find())
