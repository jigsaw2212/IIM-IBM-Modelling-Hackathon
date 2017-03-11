from multiprocessing import Pool
from pymongo import MongoClient
import glob
from functools import partial
import json
from watson_developer_cloud import DocumentConversionV1

db = MongoClient(connect=False).finhack.watson_html
document_conversion = DocumentConversionV1(
    username='b49da738-156e-4ec2-ba48-1e220df4676b',
    password='qAWnhNc1R5vs',
    version='2015-12-15'
)
config = {
    'conversion_target': 'NORMALIZED_HTML'
}


def f((i, x)):
    print '{}.1. Processing {}.'.format(i, x)
    p = x.split('/')
    doc = {}
    doc['company'] = p[-2]
    doc['_id'] = int(p[-1].rstrip('.pdf'))
    old_doc = db.find_one({'_id': doc['_id']})
    if not old_doc or 'error' in old_doc:
        try:
            print '{}.2. Calling the Document Conversion API.'.format(i)
            doc['text'] = document_conversion.convert_document(
                document=open(x, 'r'), config=config)._content
        except Exception as e:
            doc['error'] = [str(arg) for arg in e.args]
            print '{}.3. Error: {}'.format(i, e)
        update = {'$set': doc}
        if not 'error' in doc:
            update['$unset'] = {'error': ''}
        db.update_one(
            {'_id': doc['_id']}, update, upsert=True)
    print '{}.4. Processed {}.'.format(i, x)


if __name__ == '__main__':
    pool = Pool(5)
    # files = [(i, file) for i, file in enumerate(glob.glob('../DATA/**/*.pdf'))]
    # print len(files)
    files = [(i, '/'.join(('..', 'DATA', report['company'], str(report['_id']) + '.pdf')))
             for i, report in enumerate(db.find({'error': {'$exists': True}}))]
    # print files
    pool.map(f, files)
    # [f(file) for file in files]
