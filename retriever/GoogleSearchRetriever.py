import sys
import pickle
from urllib.parse import unquote
#from googlesearch import search
import numpy as np
import requests
import json
import urllib

class ScrapGoogleSearchRetriever:
    """
    This uses the python library google, this library does a web scrape and thus only works for small requests
    """
    def __init__(self, docs, k=5):
        """
        :param docs: dictionary form of Wikipedia
        :param k:  number of articles to return
        """
        self.k = k
        self.docs = docs

    def get_topk_docs(self, query):
        urls = search('site:ar.wikipedia.org' +" " +str(query), stop=self.k, domains=["ar.wikipedia.org"])
        article_titles = []
        for url in urls:
            article_titles.append(unquote(url[30:]).replace("_"," "))
        top_docs = []
        for title in article_titles:
            if title in self.docs:
                top_docs.append(self.docs[title])
            else:
                top_docs.append([""])
        return top_docs[:min(self.k,len(top_docs))]


class ApiGoogleSearchRetriever:
    """
    We call the official Google Custom Search API, need to obtain API Key first and CSE, $5 per 5000requests
    """
    def __init__(self, docs, k=5):
        """
        :param docs: dictionary form of Wikipedia
        :param k:  number of articles to return
        """
        self.k = min(k, 10) # API has max 10 results
        self.docs = docs
        # custom search engine ID, need to create on cloud shell
        self.CSE = ""
        # API KEY for custom search
        self.API_KEY = ""

    def get_topk_docs_scores(self, query):
        query = urllib.parse.quote_plus(query)
        url = "https://www.googleapis.com/customsearch/v1/siterestrict?q=" + str(query) + "&cx=" + self.CSE\
              + "&num=" + str(self.k) + "&siteSearch=ar.wikipedia.org&key=" + self.API_KEY
        S = requests.Session()
        R = S.get(url=url, verify=False)
        DATA = R.json()
        article_titles = []
        if "items" not in DATA:
            return None, None
        for title in DATA["items"]:
            title_fixed = title['title'].replace(" - ويكيبيديا، الموسوعة الحرة","")
            if title_fixed in self.docs:
                article_titles.append(title_fixed)
        top_docs = []
        docs_scores = []
        rank = 1
        for title in article_titles[:min(self.k, len(article_titles))]:
            if title in self.docs:
                for par in self.docs[title][:15]:
                    if len(par) >= 50:
                        top_docs.append(par)
                        docs_scores.append(1/rank)
            rank += 1
        norm_cst = np.sum(1/np.arange(1,rank))
        docs_scores = np.asarray(docs_scores)
        docs_scores = docs_scores / norm_cst
        if len(top_docs) < 1:
            print("Help me I didn't find any docs")
        return top_docs, docs_scores

    def get_topk_docs(self, query):
        query = urllib.parse.quote_plus(query)
        url = "https://www.googleapis.com/customsearch/v1/siterestrict?q=" + str(query) + "&cx=" + self.CSE\
              + "&num=" + str(self.k) + "&siteSearch=ar.wikipedia.org&key=" + self.API_KEY
        S = requests.Session()
        R = S.get(url=url)#, verify=False)
        DATA = R.json()
        article_titles = []
        if "items" not in DATA:
            return []
        for title in DATA["items"]:
            title_fixed = title['title'].replace(" - ويكيبيديا، الموسوعة الحرة","")
            article_titles.append(title_fixed)

        top_docs = []
        for title in article_titles:
            if title in self.docs:
                top_docs.append(self.docs[title])
            else:
                top_docs.append([""])
        return top_docs[:min(self.k,len(top_docs))]

def test_GoogleSearchRetriever():
    wiki_data = pickle.load(open("../arwiki/arwiki.p","rb"))
    r = ApiGoogleSearchRetriever(wiki_data,5)
    print(r.get_topk_docs_scores("في اي عام كان رفع معدل النمو ل 2.2%"))


