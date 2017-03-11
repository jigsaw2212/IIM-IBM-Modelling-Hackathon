import gensim
from pymongo import MongoClient
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import re
# from nltk.corpus import stopwords
# import enchant

# dict = enchant.Dict("en_US")

db = MongoClient(connect=False).finhack

# stops = set(stopwords.words('english'))


def clean(text):
    # text = text.encode('ascii', errors='ignore')
    # text = re.sub(r'\b[^\x00-\x7F]+\b', '', text)
    text = re.sub(r'\b\d+\b', '', text)
    # Maybe change this later to replace two or more spaces/new lines with one?
    # text = re.sub(r'[\s]+', ' ', text)
    return text


def lower(words):
    return list(word.lower() for word in words)


# def only_in_dict(words):
#     try:
#         return [w for w in words if len(w) > 1 and dict.check(w) or len(w) == 1]
#     except Exception as e:
#         print list(words)
#         print w
#         raise


# def remove_stop_words(sent):
#     return list(set(sent) - stops)


class SentenceIterator(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def __iter__(self):
        for i in range(4):
            for j, doc in enumerate(db[self.prefix + str(i)].find()):
                if j % 100000 == 0:
                    print(i, j)
                if len(doc['dict_sent']['tokens']) > 10:
                    yield gensim.models.doc2vec.TaggedDocument(word_tokenize(doc['raw_sent']['text']), tags=[str(i) + '_' + str(doc['_id'])])
                else:
                    continue

sentences = SentenceIterator('senti')
model = gensim.models.doc2vec.Doc2Vec(
    size=300, min_count=5, iter=20, window=10)
print 'Building Vocab.'
model.build_vocab(sentences)
print 'Training.'
model.train(sentences)
model.save(
    'doc_vectors_raw_english')

# model = gensim.models.doc2vec.Doc2Vec.load(
#     'doc_vectors_with_lowercase_english_words_and_no_numbers')

# print model.similar_by_word("predict")

# print model.docvecs.most_similar(positive=["58c19faeb0a27c38bd5a2201"])

# print model.syn0.shape
