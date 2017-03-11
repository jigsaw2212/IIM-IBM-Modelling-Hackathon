from multiprocessing import Pool
from pymongo import MongoClient
import glob
import textract
import traceback
from wand.image import Image
from PIL import Image as PI
import pytesseract
import io

db = MongoClient(connect=False).finhack
text_db = db.textract_pdftotext2
ocr_db = db.ocr_text


# def f(x):
#     print x
#     p = x.split('/')
#     doc = {'_id': int(p[-1].rstrip('.pdf')), 'company': p[-2]}
#     if not db.find_one(doc):
#         try:
#             doc['text'] = textract.process(x)
#             doc['status'] = 'OK'
#         except Exception as e:
#             doc['status'] = 'ERROR'
#             doc['error'] = str(e)
#         db.insert_one(doc)
#         print x

def f(x):
    id, page = x.split('/')[-1].rstrip('.pdf').split('_')
    print '0. {}'.format(x)
    id = int(id)
    doc = text_db.find_one({'_id': id})
    new = False
    if not doc or not page in doc:
        try:
            text = textract.process(x)
            new = True
            print '1. {}, Textracted text.'.format(x)
        except Exception as e:
            print x, e
            text = str()
    else:
        text = doc[page]
    if len(text) <= 100:
        print '2. {}, Entering OCR.'.format(x)
        ocr_doc = ocr_db.find_one({'_id': id})
        if ocr_doc and page in ocr_doc:
            print '3. {}, Found OCR doc.'.format(x)
            text = ocr_doc[page]
        else:
            print '4. {}, Performing OCR.'.format(x)
            jpeg = Image(
                filename=x, resolution=300).convert('jpeg')
            i = Image(image=jpeg.sequence[0]).make_blob('jpeg')
            text = pytesseract.image_to_string(
                PI.open(io.BytesIO(i)), lang='eng')
        new = True
        print '5. {}, Finished OCR, new length is {}.'.format(x, len(text))
    if text and new:
        text_db.update_one({'_id': id}, {
            '$set': {page: text}, '$setOnInsert': {'_id': id}}, upsert=True)


if __name__ == '__main__':
    pool = Pool(20)
    files = [file for file in glob.glob('/home/ramparkash/PAGES/**/*.pdf')]
    [f(file) for file in files]
    pool.map(f, files)
