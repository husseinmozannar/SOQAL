# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import  nltk
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append(os.path.abspath("../embedding"))
from fasttext_embedding import fastTextEmbedder
# from elmo_embedding import elmo_embedding
# from bert_embedding import bert_embedding
# # bert-serving-start -model_dir "C:/Users/Hussein/Documents/Research/FYP-Arabic NLP/bert/multilingual_L-12_H-768_A-12" -num_worker=1

class embeddingReader:
    def __init__(self, embedder):
        self.embedder = embedder

    def concatenateString(self, paragraph, start, length):
        final_string = paragraph[start]
        for i in range(1, length):
            final_string += " " + paragraph[start + i]
        return final_string

    def get_answer_canditates(self, paragraph):
        para_sents = nltk.sent_tokenize(paragraph)
        candidates = []
        for sent in para_sents:
            para_words = sent.split()
            for i in range(0, len(para_words)):
                for j in range(1, min(15, len(para_words) - i + 1)):
                    candidate = self.concatenateString(para_words, i, j)
                    candidates.append(candidate)
        return candidates

    def read(self, P, Q):
        A = self.get_answer_canditates(P)
        A_embed = []
        for a in A:
            A_embed.append(self.embedder.embed(a))
        Q_embed = self.embedder.embed(Q)
        similarities_raw = cosine_similarity(A_embed, Q_embed.reshape(1, -1))
        similarities = [s[0] for s in similarities_raw]
        indices_sorted = np.argsort(similarities)[::-1]  # reverse order
        return A[indices_sorted[0]]
