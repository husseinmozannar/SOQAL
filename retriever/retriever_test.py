import json
import random
import pickle
from WikipediaRetriever import WikipediaRetriever
from GoogleSearchRetriever import ApiGoogleSearchRetriever
from TfidfRetriever import TfidfRetriever, HierarchicalTfidf
import sys,os
sys.path.append(os.path.abspath("../embedding"))
from fasttext_embedding import fastTextEmbedder
from EmbeddingRetriever import EmbeddingRetriever
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--ret-path', help='Retriever Path', required=True)

def accuracy_retriever(retriever, dataset):
    with open(dataset) as f:
        dataset = json.load(f)['data']
    found_answers = 0
    total_answers = 0
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                for answer in qa['answers']:
                    docs = retriever.get_topk_docs(qa['question'])
                    for doc in docs:
                        if doc.find(answer['text']) != -1:
                            found_answers += 1
                            break
                    total_answers += 1
        print("Found answers so far: " + str(found_answers))
        print("Total answers so far: " + str(total_answers))
    print("####################################################")
    print("DONE")
    print("####################################################")
    print("Found answers: " + str(found_answers))
    print("Accuracy is: " + str(found_answers / total_answers))
    return found_answers, total_answers




def accuracy_TfidfRetriever(ret_path):
    r = pickle.load(open(ret_path, "rb"))
    dataset_path = "../data/arcd.json"
    accuracy_retriever(r, dataset_path)

def accuracy_Hierarchical(ret_path):
    base_r = pickle.load(open(ret_path, "rb"))
    dataset_path = "../data/arcd.json"
    r = HierarchicalTfidf(base_r, 50, 10)
    accuracy_retriever(r, dataset_path)


def main():
    args = parser.parse_args()
    print("Evaluating TF-IDF Retriever ...")
    accuracy_TfidfRetriever(args.ret_path)
    print("Evaluating Hierarchical TF-IDF Retriever ...")
    accuracy_Hierarchical(args.ret_path)


if __name__ == "__main__":
    main()
