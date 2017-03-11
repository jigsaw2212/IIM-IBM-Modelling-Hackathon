from multiprocessing import Pool
from pymongo import MongoClient
import functools
import nltk
import re
import string

db = MongoClient(connect=False).finhack

punct = re.compile('[%s]' % re.escape(string.punctuation))


def clean(text):
    # text = text.encode('ascii', errors='ignore')
    # text = re.sub(r'\b[^\x00-\x7F]+\b', '', text)
    text = punct.sub(' ', text)
    text = re.sub(r'\b\d+\b', '', text)
    # Maybe change this later to replace two or more spaces/new lines with one?
    # text = re.sub(r'[\s]+', ' ', text)
    return text


def lower(words):
    return list(word.lower() for word in words)


def f(i, doc):
    for k in ('raw_sent', 'dict_sent'):
        doc[k]['tokens'] = lower(
            nltk.tokenize.word_tokenize(clean(doc[k]['text'])))
    db['senti' +
        str(i)].update_one({'_id': doc['_id']}, {'$set': doc})


if __name__ == '__main__':
    pool = Pool(10)
    for i in range(4):
        sent_db = db['senti' + str(i)]
        print i
        pool.map(functools.partial(f, i), sent_db.find())
        # functools.partial(f, i)(sent_db.find_one())
