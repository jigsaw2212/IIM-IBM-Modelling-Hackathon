from multiprocessing import Pool
from pymongo import MongoClient
import json
import glob
from functools import partial
# from watson_developer_cloud import AlchemyLanguageV1
from alchemy.alchemy_dao import AlchemyDAO

db = MongoClient(connect=False).finhack

watson_text = db.watson_text
alchemy_text = db.alchemy_text

alchemy_dao = AlchemyDAO()


# def f(d):
#     print alchemy.analyze(d['text'])
#     # def f((i, x)):
#     #     print '{}.1. Processing {}.'.format(i, x)
#     #     p = x.split('/')
#     #     doc = {}
#     #     doc['company'] = p[-2]
#     #     doc['_id'] = int(p[-1].rstrip('.pdf'))
#     #     old_doc = db.find_one({'_id': doc['_id']})
#     #     if not old_doc or 'error' in old_doc:
#     #         try:
#     #             print '{}.2. Calling the Alchemy PI.'.format(i)
#     #             doc['text'] = document_conversion.convert_document(
#     #                 document=open(x, 'r'), config=config)._content
#     #         except Exception as e:
#     #             doc['error'] = [str(arg) for arg in e.args]
#     #             print '{}.3. Error: {}'.format(i, e)
#     #         update = {'$set': doc}
#     #         if not 'error' in doc:
#     #             update['$unset'] = {'error': ''}
#     #         db.update_one(
#     #             {'_id': doc['_id']}, update, upsert=True)
#     #     print '{}.4. Processed {}.'.format(i, x)


# alchemy_language = AlchemyLanguageV1(api_key='1710f13c702a37f5d2ba70bb55bc98928b32edcb')


# def f((x, y)):
# print alchemy_language.combined(text=y[0]['text'],
# extract='entities,keywords', sentiment=1)

def f(doc):
    print doc['company'], doc['_id']
    text = watson_text.find_one({'_id': doc['_id']}).pop('text')
    alchemy_analysis = alchemy_dao.analyze(text)
    if alchemy_analysis['status'] == 'ERROR':
        print alchemy_analysis['statusInfo']
    alchemy_text.update_one(
        {'_id': doc['_id']}, {'$set': dict(doc, **alchemy_analysis)})


if __name__ == '__main__':
    pool = Pool(5)
    docs = list(alchemy_text.find(
        {'status': 'ERROR', 'statusInfo': {'$ne': 'unsupported-text-language'}}))
    pool.map(f, docs)
    # [f(file) for file in files]
