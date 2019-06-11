# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import random
import nltk

class RandomReader:
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

    def read(self, P , Q):
        A = self.get_answer_canditates(P)
        answer = A[random.randint(0,len(A)-1)]
        return  answer



