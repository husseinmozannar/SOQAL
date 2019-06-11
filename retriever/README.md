## Document Retrievers

We have implemented four different document retrievers that given a document set (constrained to Arabic Wikipedia for API based methods) and a query return the top k most relevant documents to the query:

*  TF-IDF Retriever: classical TF-IDF retrieval based on n-grams: TfidfRetriever in TfidfRetriever.py

*  **Hierarchical TF-IDF Retriever**: fully described in our paper, relies on two chained TF-IDF retrievers sequentially narrowing the search space: HierarchicalTfidf in TfidfRetriever.py

*  Wikipedia API search Retreiver: calls the Wikipedia API for the search query: WikipediaRetriever in WikipediaRetriever.py

*  Google Custom Search Engine Retriever (restricted to Wikipedia): ApiGoogleSearchRetriever in GoogleSearchRetriever.py

*  Embedding Retriever: computes for each document a representation using the sum of its word
embeddings, documents are ranked with respect to cosine similarity: EmbeddingRetriever in EmbeddingRetriever.py


All retrievers are built as Python classes with almost the same implementation: the constructor takes in a python list of string documents or a python dictionary of the documents and the method get_topk_docs returns the topk documents for a string query.

## Building a TF-IDF Retriever

To build a TF-IDF retriever first make sure you have a pickled version of Wikipedia by following the instructions in [build Python Wikipedia](../arwiki/README.md).

Then run the following:
```shell
python Tfidfretriever ^
-n NGRAMS ^
-k TOPK ^
-w arwiki.p ^
-o OUPUT_DIR
```
Arguments: -n: "n"-grams , -k: number of articles to return, -w: path of arwiki.p, -o: output directory to place the pickled retriever

It will create a 2GB file called "tfidfretriever.p" in your OUTPUT_DIR if you used 1-grams. Expect 5GB for bigrams.

## Evaluating The TF-IDF Retriever on ARCD

To obtain the accuracy of the TF-IDF retriever and Hierarchical retriever with the built retriever as base, simply run:

```shell
python retriever_test.py -r path/to/tfidfretriever.p
```

You should get with a 1-gram TF-IDF and k=10 about  58.2% (much higher than reported in the paper as we changed stemmer). It takes 15 mins or so to get these results.

With the Hierarchical retriever with a base 1-gram k=100 retriever and returning 10 documents expect  . The evaluation will take a couple of hours as this implementation is not optimized for testing (you can do it much more quickly).



