from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.arlstem import ARLSTem
from nltk.corpus import stopwords
import numpy as np
import pickle
class fastTextEmbedder:
    def __init__(self, model_path):
        self.model_path = model_path
        print("loading fastText model ...")
        #self.model = pickle.load(open(self.model_path,"rb"))
        self.model = KeyedVectors.load_word2vec_format(self.model_path, encoding='utf-8', unicode_errors='ignore')
        print("done fastText loading model")
        self.tokenizer = WordPunctTokenizer()
        self.stemmer = ARLSTem()
        self.SYMBOLS = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\"'
        self.vocab = self.model.vocab

    def tokenize_string(self, str):
        """
        :param str: string sentence
        :return: tokens stemmed with respect to nltk
        """
        str_tokens = self.tokenizer.tokenize(str)
        tokens_stemmed = []
        for token in str_tokens:
            has_symbol = False
            for s in self.SYMBOLS:
                if s in token:
                    has_symbol = True
                    break
            if not has_symbol:
                tokens_stemmed.append((token, self.stemmer.stem(token)))
        return tokens_stemmed


    def embed_tokens(self, sent, max_len):
        sent_tokens = self.tokenize_string(sent)
        embedding = np.zeros((max_len,300))
        i = j = 0
        for i in range(0,min(len(sent_tokens),max_len)):
            e = np.zeros(300)
            if sent_tokens[i][0] in self.vocab:
                embedding[j] = self.model[sent_tokens[i][0]]
                j += 1
            elif sent_tokens[i][1] in self.vocab:
                embedding[j] = self.model[sent_tokens[i][1]]
                j += 1
        return embedding

    def embed(self, sent):
        """
        :param sent: string sentence
        :return: embedding of sentence as np vector of dim=300
        """
        sent_tokens = self.tokenize_string(sent)
        embedding = np.zeros(300)
        for token in sent_tokens:
            if token[0] in self.vocab:
                embedding += self.model[token[0]]
            elif token[1] in self.vocab:
                embedding += self.model[token[1]]
        return embedding



def Test_fastTextEmbedder():
    e = fastTextEmbedder("cc.ar.300.vec")
    print(e.embed( "نادي ليفربول"))
    print(e.embed("Dadadadda"))
    print(e.embed("الباراسيتامول (بالإنجليزية: Paracetamol) أو الأسيتامينوفين (بالإنجليزية: Acetaminophen) هو مسكن ومخفض للحرارة"))
    print(e.embed_tokens("أزمة المياه هي حالة الموارد المائية",50))
    print(e.embed_tokens("أزمة المياه هي حالة الموارد المائية",50).shape)
