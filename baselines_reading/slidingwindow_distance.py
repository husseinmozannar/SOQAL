from nltk.tokenize import WordPunctTokenizer
from nltk.stem.arlstem import ARLSTem
from nltk.corpus import stopwords
from math import log
import nltk


class SWDbasline:
    def __init__(self):
        self.tokenizer = WordPunctTokenizer()
        self.stemmer = ARLSTem()
        self.SYMBOLS = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\"'

    def tokenize_string(self, str):
        str_tokens = self.tokenizer.tokenize(str)
        tokens_stemmed = []
        for token in str_tokens:
            has_symbol = False
            for s in self.SYMBOLS:
                if s in token:
                    has_symbol = True
                    break
            if not has_symbol:
                tokens_stemmed.append(self.stemmer.stem(token))
        return tokens_stemmed

    def IC(self, w, P):
        return log(1 + 1/self.C(w, P), 2)

    def C(self, w, P):
        sum = 0
        for word in P:
            if word == w:
                sum += 1
        return sum

    def sliding_window_helper(self, P, Q, A):
        res = []
        for i in range(0, len(A)):
            S = list(set().union(Q, A[i]))
            cur = 0
            for j in range(0, len(P) - len(S) + 1):
                sum = 0
                for w in range(0, len(S)):
                    if P[j + w] in S:
                        sum += self.IC(P[j + w], P)
                cur = max(cur, sum)
            res.append(cur)
        return res

    def sliding_window(self, P, Q, A):
        return self.sliding_window_helper(self.tokenize_string(P), self.tokenize_string(Q), A)

    def dist(self, P, q, a):
        res = len(P) + 1
        for i in range(0, len(P)):
            if P[i] == q or P[i] == a:
                if P[i] == q:
                    a, q = q, a
                index = self.find_after(P, q, i)
                if index != -1:
                    res = min(res, index - i)
        return res

    def find_after(self, L, w, i):
        for j in range(i, len(L)):
            if(L[j] == w):
                return j
        return -1

    def distance_based_helper(self, P, Q, A):
        res = []
        U = set(stopwords.words('arabic')) & set(P)
        SQ = list(set(P) & set(Q) - U)
        for i in range(0, len(A)):
            SA = list(((set(A[i]) & set(P)) - set(Q)) - U)
            d = len(P) + 1
            if(len(SQ) == 0 or len(SA) == 0):
                d = 1
            else:
                for q in SQ:
                    for a in SA:
                        d = min(d, self.dist(P, q, a))
            d *= 1 / (len(P) - 1)
            res.append(d)
        return res

    def distance_based(self, P, Q, A):
        return self.distance_based_helper(self.tokenize_string(P), self.tokenize_string(Q), A)

    def argmax(self, l):
        return l.index(max(l))

    def SW(self, P, Q, A):
        return self.argmax(self.sliding_window(P, Q, A))

    def concatenateString(self, paragraph, start, length):
        final_string = paragraph[start]
        for i in range(1, length):
            final_string += " " + paragraph[start + i]
        return final_string

    def get_answer_canditates(self, paragraph):
        candidates = nltk.sent_tokenize(paragraph)
        return candidates

    def read_score(self, P, Q):
        """
        Implemnts SWD algorithm
        :param P: paragraph string
        :param Q: question string
        :return: answer index
        """
        A = self.get_answer_canditates(P)
        ret_sw = self.sliding_window(P, Q, A)
        ret_d = self.distance_based(P, Q, A)
        max_indx = self.argmax([x - y for x, y in zip(ret_sw, ret_d)])
        max_val = max([x - y for x, y in zip(ret_sw, ret_d)])
        return A[max_indx], abs(max_val)


    def read(self, P, Q):
        """
        Implemnts SWD algorithm
        :param P: paragraph string
        :param Q: question string
        :return: answer index
        """
        A = self.get_answer_canditates(P)
        ret_sw = self.sliding_window(P, Q, A)
        ret_d = self.distance_based(P, Q, A)
        return A[self.argmax([x - y for x, y in zip(ret_sw, ret_d)])]


def test_SWD():
    reader = SWDbasline()
    print(reader.read_scores("My name is hussein and my father work at the university. My mother was a murderer, she killed my father",
        "What is my"))

#test_SWD()