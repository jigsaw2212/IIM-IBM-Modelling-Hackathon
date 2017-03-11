from multiprocessing import Pool
from pymongo import MongoClient
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from nltk.corpus import stopwords
import enchant

db = MongoClient(connect=False).finhack

text_db = db.textract_pdftotext2

stopwords = stopwords.words('english')

dict = enchant.Dict("en_US")


def clean(text):
    text = text.encode('ascii', errors='ignore')
    # text = re.sub(r'\b[^\x00-\x7F]+\b', '', text)
    # text = re.sub(r'\b\d+\b', '', text)
    # Maybe change this later to replace two or more spaces/new lines with one?
    # text = re.sub(r'[\s]+', ' ', text)
    return text


def f(doc):
    id = doc.pop('_id')
    print id
    j = 0
    sent_db = db['sent' + str(j)]
    for page in doc.keys():
        text = clean(doc[page])
        for i, sent in enumerate(sent_tokenize(text)):
            sent_doc = {'doc_id': id, 'page_no': int(page), 'sent_no': i}
            sent_doc['raw_sent'] = sent
            words = word_tokenize(sent)
            sents = {}
            # sents['small_sent'] = lower(words)
            sents['dict_sent'] = only_in_dict(words)
            # sents['small_dict_sent'] = only_in_dict(sents['small_sent'])
            # sents['wo_stopwords_sent'] = remove_stop_words(
            #     sents['small_sent'])
            # sents['wo_stopwords_dict_sent'] = remove_stop_words(
            # sents['dict_sent'])
            for k in sents:
                sent_doc[k] = ' '.join(sents[k])
            while sent_db.count() >= 500000:
                j += 1
                sent_db = db['sent' + str(j)]
            sent_db.insert_one(sent_doc)


def lower(words):
    return (word.lower() for word in words)


def only_in_dict(words):
    ret = []
    for w in words:
        try:
            if dict.check(w):
                ret.append(w)
        except Exception as e:
            print e, w
    return ret


def remove_stop_words(sent):
    return (w for w in sent if w not in stopwords)


if __name__ == '__main__':
    pool = Pool(10)
    pool.map(f, text_db.find())
    # f(text_db.find_one())
