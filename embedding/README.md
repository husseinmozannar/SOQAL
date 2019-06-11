## Embedding Helpers

To load and use fastText embeddings for the retriever and reader please first download the fastText text file from:
https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.af.300.vec.gz


We have made an easy interface to use embeddings in any code with the class *fastTextEmbedder* found in fasttext_embedding.py

Here is a code example to embed a string sentence:
```
embedder = fastTextEmbedder("cc.af.300.vec") # location of the file downloaded
example = "نادي ليفربول"
embedded_example = embedder.embed(example) # returns 300 dimensional vector
```

We **really** recommend pickling the fastText model for later use,  loading for the fastText is very slow and no other solution exists for Windows at least.
