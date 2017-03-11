from pymongo import MongoClient
import pdb

client = MongoClient()
db = client['finhack']
collection = db.fls2
cur = collection.find({})

for doc in cur:
	comp_id = str(int(doc['_id']))[:6]
	doc['comp_id'] = comp_id
	collection.update({"_id": doc['_id']},doc)
