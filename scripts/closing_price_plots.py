import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pdb
from sklearn import preprocessing
from sklearn.cluster import SpectralClustering
from pymongo import MongoClient

client = MongoClient()
db = client['finhack']
collection = db.fls2

CSV_PATH	=	"/home/ramparkash/Data/StockData/"
FILES		= 	os.listdir(CSV_PATH)
FILES		=	[CSV_PATH+f for f in FILES]
means		= 	list()
input_means	= 	list()
all_data	=	list()

for ind,csv_file in enumerate(FILES):
	print ind
	df  		=	pd.read_csv(csv_file)
	try:
		df['Date']	= 	df['Date'].apply(pd.to_datetime)
	except Exception as e:
		continue
	diff  = df['Date'][df.index[-1]] - df['Date'][0]
	diff = abs(diff.days)
	new_df = pd.Series(pd.date_range(df['Date'][df.index[-1]],periods=diff,freq='D'))
	new_df = pd.DataFrame({'Date': new_df})
	df = pd.merge(new_df,df[['Date','Close Price']],on='Date',how='left')
	df['Close Price'].fillna((df['Close Price'].mean()), inplace = True)
	min_max_scaler	= 	preprocessing.MinMaxScaler()
	try:
		np_scaled	= 	pd.DataFrame(min_max_scaler.fit_transform(df["Close Price"]))
		means.append(list(np_scaled.rolling(window=365).mean().values.flatten()))
	except Exception as e:
		continue

for m in means:
	input_means.append(m)

num_clusters 	=	30


input_means	=	np.array(input_means)
input_means	=	np.nan_to_num(input_means)

print 'Gonna plot bitch'

for i in range(len(input_means)):
	try:
		x = int(FILES[i].split('/')[-1].rstrip('.csv'))
	except Exception as e:
		continue
	cur = db.fls2.find({"comp_id": str(x) })	
	sent_pos = []
	sent_neg = []
	sent_neu = []
	sent_comp = []
	for doc in cur:
		pos = 0
		neg = 0
		neu = 0
		comp = 0
		for fls in doc['fls']:
			pos += fls['sentiment']['pos']
			neg += fls['sentiment']['neg']
			neu += fls['sentiment']['neu']
			comp += fls['sentiment']['compound']
		sent_pos.append(pos)
		sent_neg.append(neg)
		sent_neu.append(neu)
		sent_comp.append(comp)
	sent_pos = [s/max(sent_pos) for s in sent_pos]
	sent_neg = [s/max(sent_neg) for s in sent_neg]
	sent_neu = [s/max(sent_neu) for s in sent_neu]
	try:
		scaler = preprocessing.MinMaxScaler()
		sent_comp = [s/max(sent_comp) for s in sent_comp]
		sent_comp = scaler.fit_transform(sent_comp)
	except Exception as e:
		continue
	
	try:
		plt.xlabel('Time')
		plt.ylabel('Sentiment/Close Price')
		plt.grid(True)	
		#plt.plot(range(365,365*(len(sent_pos)+1),365),sent_comp,color='green')
		plt.plot(range(365,365*(len(sent_pos)+1),365),sent_pos,color='y')
		#plt.plot(range(365,365*(len(sent_neu)+1),365),sent_neu,color='blue')
		#plt.plot(range(365,365*(len(sent_neg)+1),365),sent_neg,color='red')
		plt.plot(range(len(input_means[i])),input_means[i],color='violet')
		plt.savefig("plots/"+str(FILES[i].split('/')[-1].rstrip('.csv'))+'.png')
		plt.clf()
	except Exception as e:
		plt.clf()
		continue
