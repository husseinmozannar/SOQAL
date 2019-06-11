## Non-Learning Baseline Readers
We have implemented three basic baseline readers. Each given a paragraph and a question generates an answer from the paragraph.
They do so by ranking every text span of lenght maximally 10 words inside each sentence. The methods are:

*  Sliding Window Distance based reader (Richardson et al. 2013) SWDbasline in "slidingwindow_distance.py"
*  TF-IDF reader based on 4-gram features TfidfReader in "tfidf_reader.py"
*  Embedding approach where the candidate with
the highest cosine similarity with respect to fast-
Text embeddings is returned, embeddingReader in "embedding_match.py"

All three have the same functions: method read(P, Q) which takes in a paragraph and question and return as string the answer. However TfidfReader needs first to be initialized.


## Evaluating the Baselines on the Arabic Reading Comprehension Dataset

We have provided a script to replicate the results of the baselines on the Arabic Reading Comprehension Dataset found in the data folder.

Make sure to follow the instructions in [embedding README](../embedding/README.md) to run the embedding reader, provide the path of the cc.ar.300.vec as EMBEDDING_PATH.

Simply run the following:
```shell
python evaluate_baselines.py  -e EMBEDDING_PATH
```

You should get similar results to those in the paper:

Methods |  EM  | F1 | SM
------------------------------------- | :------: | :------: | :------:
Random Reader            | 0.07 | 8.13 | 51.0
TF-IDF Reader            | 0.22 | 5.6 | **75.3**
Embedding Reader            | **0.36** | **15.3** | 73.1
SWD Reader         | 0.07 | 14.2 | 58.4


