import requests
import json
import pickle
import numpy as np

class WikipediaRetriever:
    """
    Retreiver using the official Wikipedia API
    """
    def __init__(self, docs, k):
        """
        :param docs: dictionary form of Wikipedia
        :param k:  number of articles to return
        """
        self.S = requests.Session()
        self.URL = "https://ar.wikipedia.org/w/api.php"
        self.k = k
        self.docs = docs

    def get_topk_docs_scores(self, query):
        PARAMS = {
            'action': "query",
            'list': "search",
            'srsearch': query,
            'format': "json"
        }
        R = self.S.get(url=self.URL, params=PARAMS)
        DATA = R.json()
        L = DATA['query']['search']
        article_titles = []
        for i in range(0, len(L)):
            if L[i]['title'] in self.docs:
                article_titles.append(L[i]['title'])
        top_docs = []
        docs_scores = []
        rank = 1
        for title in article_titles[:min(self.k, len(article_titles))]:
            if title in self.docs:
                for par in self.docs[title]:
                    if len(par)>100:
                        top_docs.append(par)
                        docs_scores.append(1/rank)
            rank += 1
        docs_scores = np.asarray(docs_scores)
        docs_scores = docs_scores / docs_scores.sum(axis=0, keepdims=1)
        return top_docs, docs_scores

    def get_topk_docs(self, query):
        PARAMS = {
            'action': "query",
            'list': "search",
            'srsearch': query,
            'format': "json"
        }
        R = self.S.get(url=self.URL, params=PARAMS)
        DATA = R.json()
        L = DATA['query']['search']
        article_titles = [""] * len(L)
        for i in range(0, len(L)):
            article_titles[i] = L[i]['title']
        top_docs = []
        for title in article_titles:
            if title in self.docs:
                top_docs.append(self.docs[title])
        return top_docs[:min(self.k, len(top_docs))]


def test_WikipediaRetriever():
    wiki_data = pickle.load(open("../wiki_extractor/arwiki.p", "rb"))
    r = WikipediaRetriever(wiki_data, 5)
    print(r.get_topk_docs_scores("نادي ليفربول"))

#test_WikipediaRetriever()
