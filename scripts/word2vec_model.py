import gensim
from pymongo import MongoClient
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from nltk.corpus import stopwords
import enchant
from nltk.stem import WordNetLemmatizer
import string

# wordnet_lemmatizer = WordNetLemmatizer()

# dict = enchant.Dict("en_US")

db = MongoClient(connect=False).finhack

stops = set(stopwords.words('english'))

punct = re.compile('[%s]' % re.escape(string.punctuation))


def clean(text):
    text = text.encode('ascii', errors='ignore')
    text = re.sub(r'\b[^\x00-\x7F]+\b', '', text)
    # text = re.sub(r'\b\d+\b', '', text)
    # text = punct.sub(' ', text)
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


def remove_stop_words(sent):
    return list(set(sent) - stops)


# def lemmatize(words):


class SentenceIterator(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def __iter__(self):
        for i in range(4):
            for j, doc in enumerate(db[self.prefix + str(i)].find()):
                if j % 100000 == 0:
                    print(i, j)
                yield lower(word_tokenize(clean(doc['raw_sent']['text'])))
                # yield lower(word_tokenize(clean(doc['dict_sent'])))

sentences = SentenceIterator('senti')

model = gensim.models.Word2Vec(workers=20, size=300)
print 'Building Vocab.'
model.build_vocab(sentences)
print 'Training.'
model.train(sentences)
# model = gensim.models.Word2Vec.
model.save(
    'word_vectors_raw_eng_lowercase')


# model = gensim.models.Word2Vec.load(
#     'word_vectors_raw_eng')

# print model.most_similar(positive=['programming', 'Zee'], topn=20)
