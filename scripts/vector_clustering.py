from sklearn.cluster import KMeans, MiniBatchKMeans
import time
import gensim
import joblib
import numpy
from pymongo import MongoClient
from bson.objectid import ObjectId

# KMeans = MiniBatchKMeans

db = MongoClient().finhack

start = time.time()  # Start time

# Set "k" (num_clusters) to be 1/5th of the vocabulary size, or an
# average of 5 words per cluster
model = gensim.models.doc2vec.Doc2Vec.load(
    'word_vectors_raw_eng')


vectors = model.wv.syn0
# model.docvecs.doctag_syn0
# model.wv.syn0
# num_clusters = 100  # word_vectors.shape[0] / 5
# print num_clusters, vectors.shape

# # Initalize a k-means object and use it to extract centroids
# kmeans_clustering = KMeans(n_clusters=num_clusters)
# idx = kmeans_clustering.fit(vectors.astype(numpy.float64))
# joblib.dump(kmeans_clustering, '100_word_vec_raw_eng.pkl')

kmeans_clustering = joblib.load('100_word_vec_raw_eng.pkl')
for center in kmeans_clustering.cluster_centers_:
    print model.most_similar([center])
#     tags = model.docvecs.most_similar([center])
#     for tag in tags:
#         i, obj = tag[0].split('_')
#         doc = db['sent' + i].find_one({'_id': ObjectId(obj)})
#         print doc['dict_sent'], tag[1]
#     print '\n'


print kmeans_clustering.inertia_

# Get the end time and print how long the process took
end = time.time()
elapsed = end - start
print "Time taken for K Means clustering: ", elapsed, "seconds."
