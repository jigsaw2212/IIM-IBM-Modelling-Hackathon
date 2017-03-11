from pymongo import MongoClient
import json
import pdb

class NoSQL:
	def __init__(self):
		self.conn = MongoClient()
		self.db	  = self.conn['finhack']

	def find(self):
		return self.db.watson_text.find()

	def __del__(self):
		del self.db
		del self.conn

	def insert(self,obj):
		self.db.forward_looking_statements.insert_one(obj)

mongo = NoSQL()
reports = mongo.find()
foward_words = ["will","should","can","could","may","might","expect", "anticipate", "believe", "plan", "hope", "intend", "seek", "project", "forecast", "objective","goal"]
for index,doc in enumerate(reports):
	print "Report {}".format(index)
	forward_looking_statements = []
	try:
		report = doc['text']
	except Exception:
		continue
	sentences = report.split('.')
	for i,sentence in enumerate(sentences):
		print "Sentence {}".format(i)
		if len(set(sentence.split(" ")).intersection(set(foward_words))) != 0:
			forward_looking_statements.append(sentence)
	obj = {"name":doc['_id'],"forward_looking_statements":forward_looking_statements,"company_name":doc["company"]}
	mongo.insert(obj)	
