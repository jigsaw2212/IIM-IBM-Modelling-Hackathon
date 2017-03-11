from gensim.models.word2vec import Word2Vec
from sklearn.manifold import TSNE
import re
import matplotlib.pyplot as plt


model = Word2Vec.load(
    'word_vectors_with_lowercase_english_words_and_no_numbers')

X = model[model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.show()
