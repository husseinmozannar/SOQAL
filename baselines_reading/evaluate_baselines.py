from __future__ import print_function
from collections import Counter
import string
import re
import argparse
import json
import sys
import nltk
from random import randint
import argparse


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        fix_text = re.sub(r'\b(a|an|the)\b', ' ', text)
        fix_text = re.sub('\sال^|ال', ' ', fix_text)
        return fix_text
    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate(dataset, reader):
    f1 = exact_match = total = exact_sentence = inclusion = random = 0
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                total += 1
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                prediction = reader.read(paragraph['context'], qa['question'])
                sents = nltk.sent_tokenize(paragraph['context'])
                indx_g = -1
                indx_p = -1
                i = 0
                for sent in sents:
                    if sent.find(ground_truths[0]) != -1:
                        indx_g = i
                    if sent.find(prediction) != -1:
                        indx_p = i
                    i += 1
                test = randint(0, i)
                if test == indx_g:
                    random += 1
                if prediction.find(ground_truths[0]) != -1 or ground_truths[0].find(prediction):
                    inclusion += 1
                if indx_g == indx_p and indx_p != -1:
                    exact_sentence += 1
                exact_match += metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                f1 += metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)
    inclusion = 100 * inclusion / total
    random = 100 * random / total
    exact_sentence = 100 * exact_sentence / total
    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total

    return {'exact_match': exact_match, 'f1': f1, 'exact_sentence': exact_sentence, 'inclusion': inclusion,
            'random': random}


from slidingwindow_distance import SWDbasline


def evaluate_reader(dataset_path, reader):
    with open(dataset_path) as f:
        dataset = json.load(f)['data']
    print(json.dumps(evaluate(dataset, reader)))


def evaluate_SWD():
    dataset_path = "../data/arcd.json"
    reader = SWDbasline()
    evaluate_reader(dataset_path, reader)


from embedding_match import embeddingReader
import os

sys.path.append(os.path.abspath("../../embedding"))
from fasttext_embedding import fastTextEmbedder


def evaluate_embeddingReader(emb_path):
    embedder = fastTextEmbedder(emb_path)
    reader = embeddingReader(embedder)
    dataset_path = "../data/arcd.json"
    evaluate_reader(dataset_path, reader)


from tfidf_reader import TfidfReader

def evaluate_TfidfReader():
    dataset_path = "../data/arcd.json"
    with open(dataset_path) as f:
        dataset = json.load(f)['data']
    f1 = exact_match = total = exact_sentence = inclusion = random = 0
    for article in dataset:
        for paragraph in article['paragraphs']:
            reader = TfidfReader(paragraph['context'])
            for qa in paragraph['qas']:
                total += 1
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                prediction = reader.read(paragraph['context'], qa['question'])
                sents = nltk.sent_tokenize(paragraph['context'])
                indx_g = -1
                indx_p = -1
                i = 0
                for sent in sents:
                    if sent.find(ground_truths[0]) != -1:
                        indx_g = i
                    if sent.find(prediction) != -1:
                        indx_p = i
                    i += 1
                test = randint(0, i)
                if test == indx_g:
                    random += 1
                if prediction.find(ground_truths[0]) != -1 or ground_truths[0].find(prediction):
                    inclusion += 1
                if indx_g == indx_p and indx_p != -1:
                    exact_sentence += 1
                exact_match += metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                f1 += metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)
    inclusion = 100 * inclusion / total
    random = 100 * random / total
    exact_sentence = 100 * exact_sentence / total
    exact_match = 100.0 * exact_match / total
    f1 = 100.0 * f1 / total

    to_print = {'exact_match': exact_match, 'f1': f1, 'exact_sentence': exact_sentence, 'inclusion': inclusion,
                'random': random}
    print(to_print)


from random_reader import RandomReader


def evaluate_RandomReader():
    reader = RandomReader()
    dataset_path = "../data/arcd.json"
    evaluate_reader(dataset_path, reader)


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--emb', help='Location of fastText embedding .vec file', required=True)


def main():
    args = parser.parse_args()
    print('Evaluating the Random Reader ...')
    evaluate_RandomReader()
    print('Evaluating the TF-IDF Reader ...')
    evaluate_TfidfReader()
    print('Evaluating the Sliding Window Distance Based Baseline ...')
    evaluate_SWD()
    print('Evaluating an embedding based reader using fastText ...')
    evaluate_embeddingReader(args.emb)


if __name__ == "__main__":
    main()
