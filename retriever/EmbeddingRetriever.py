import nltk
from nltk.stem.arlstem import ARLSTem
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import WordPunctTokenizer
import numpy as np
import pickle
import sys,os
sys.path.append(os.path.abspath("../embedding"))
from fasttext_embedding import fastTextEmbedder

class EmbeddingRetriever:
    SYMBOLS = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\"'
    def __init__(self, docs, k, embedder, emb_matrix = None):
        """
        :param docs: list of documents as strings
        :param k:  number of documents to retrieve
        :param embedder: an embedding object that has a function embed that takes a string and outputs numpy vector
        :param emb_matrix: a matrix of embedding corresponding to the docs
        """
        self.k = k  # number of documents to return
        self.docs = docs
        self.embedder = embedder

        if emb_matrix is None:
            self.build_emb_matrix()
            print("built embedding matrix")
        else:
            self.emb_matrix = emb_matrix

    def build_emb_matrix(self):
        self.emb_matrix = []
        for doc in self.docs:
            self.emb_matrix.append(self.embedder.embed(doc))

    def embed_string(self, sent):
        return self.embedder.embed(sent)

    def get_topk_docs(self, query):
        """
        :param query: a string
        :return: top documents according to cosine similarity of embeddings
        """
        emb_query = self.embed_string(query)
        similarities_raw = cosine_similarity(self.emb_matrix, emb_query.reshape(1,-1))
        similarities = [s[0] for s in similarities_raw]
        indices_sorted = np.argsort(similarities)[::-1]  # reverse order
        topk_docs = []
        for i in range(0, self.k):
            topk_docs.append(self.docs[indices_sorted[i]])
        return topk_docs

def build_embedding_matrix_fasttext():
    wiki_data = pickle.load(open("../arwiki/arwiki.p", "rb"))
    docs = []
    for art, pars in wiki_data.items():
        for p in pars:
            docs.append(p)
    embedder = fastTextEmbedder()
    docs_embed = []
    i = 0
    for doc in docs:
        docs_embed.append(embedder.embed(doc))
        i += 1
        if i%10000 == 0:
            print("finished so far " +str(i))
    pickle.dump(docs_embed,open("fasttext_matrix.p","wb"))

