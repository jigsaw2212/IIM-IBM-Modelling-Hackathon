from multiprocessing import Pool
from pymongo import MongoClient
import functools
import nltk
db = MongoClient(connect=False).finhack


def f(i, doc):
    # print(i, j)
    for k in ('raw_sent', 'dict_sent'):
        doc[k]['pos_tags'] = nltk.pos_tag(
            nltk.tokenize.word_tokenize(doc[k]['text']))
    db['senti' +
        str(i)].update_one({'_id': doc['_id']}, {'$set': doc})


if __name__ == '__main__':
    pool = Pool(10)
    for i in range(4):
        sent_db = db['senti' + str(i)]
        pool.map(functools.partial(f, i), sent_db.find())
        # functools.partial(f, i)(sent_db.find_one())
