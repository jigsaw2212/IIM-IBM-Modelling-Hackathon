from wand.image import Image
from PIL import Image as PI
# import pyocr
# import pyocr.builders
import pytesseract
import io
import glob
import os
from multiprocessing import Pool
from pymongo import MongoClient


db = MongoClient(connect=False).finhack.ocr_text

# tool = pyocr.get_available_tools()[0]
# lang = tool.get_available_languages()[2]


def f(x):
    try:
        id, page = x.split('/')[-1].rstrip('.pdf').split('_')
        id = int(id)
        doc = db.find_one({'_id': id})
        if doc and page in doc:
            return
        jpeg = Image(
            filename=x, resolution=300).convert('jpeg')
        i = Image(image=jpeg.sequence[0]).make_blob('jpeg')
        # text = tool.image_to_string(
        #     PI.open(io.BytesIO(i)), lang=lang,
        #     builder=pyocr.builders.TextBuilder())
        text = pytesseract.image_to_string(PI.open(io.BytesIO(i)), lang='eng')
        db.update_one(
            {'_id': id}, {'$set': {page: text}, '$setOnInsert': {'_id': id}}, upsert=True)
        print x
    except Exception as e:
        print x, e


if __name__ == '__main__':
    pool = Pool(20)
    files = [file for file in glob.glob('/home/ramparkash/PAGES/**/*.pdf')]
    pool.map(f, files)
