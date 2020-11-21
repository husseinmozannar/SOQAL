# -*- coding: utf-8 -*-
# This is Python 3.6
from __future__ import division
import json

from find_answer import find_answer
from processing import transliterate_to_arabic
from multiprocessing.dummy import Pool as ThreadPool
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help='Location of Translated SQuAD', required=True)

ARABIC_LETTERS = 'ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ'


def is_arabic(text):
    for letter in text:
        if ARABIC_LETTERS.find(letter) > 0:
            return True
    return False


total = 0
def fix_answer_article(article):
    # article level fix answer for the parallel implementation
    for paragraph in article['paragraphs']:
        p = paragraph['context'].replace("&quot;","")
        p = transliterate_to_arabic(p)
        global total
        total += 1
        if (total%10 ==0):
            print(total)
        paragraph['context'] = p
        for qa in paragraph['qas']:
            for answer in qa['answers']:
                ba = transliterate_to_arabic(answer['text'])
                proposed_answer, answer_start = find_answer(p, ba)
                answer['text'] = proposed_answer
                if answer_start >= 0:
                    answer['answer_start'] = answer_start
                else:
                    answer['answer_start'] = 0
    return article


def fix_answers_parallel(filename):
    # fix answers in a parallel way with ThreadPool, speed up is immense
    with open(filename) as f:
        dataset = json.load(f)['data']
    pool = ThreadPool(100)
    new_data = pool.map(fix_answer_article, dataset)
    new_data = {
        'data': new_data,
        'version': "1.1"
    }
    with open(filename[:-5] + "_fixed_answers.json", 'w') as fp:
        json.dump(new_data, fp)


def concatenateString(paragraph, start, length):
    if start>len(paragraph) or len(paragraph)-start<length:
        return ""
    final_string = paragraph[start]
    for i in range(1, length):
        final_string += paragraph[start + i]
    return final_string

def fix_answers(filename, only_count=True):
    # fix answers using findAnswer module, if only_count is True only counts the bad answers
    answers = 0
    valid_answers = 0
    with open(filename) as f:
        dataset = json.load(f)['data']
    new_data = []
    for article in dataset:
        print(article['title'])
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                for answer in qa['answers']:
                    answers += 1
                    if only_count:
                        paragraph['context'] = paragraph['context'].replace("  "," ")
                        paragraph['context'] = paragraph['context'].replace("  "," ")
                        answer['answer_start']= paragraph['context'].find(answer['text'])
                        ans = concatenateString(paragraph['context'],answer['answer_start'],len(answer['text']))
                        if ans == answer['text']:
                            valid_answers += 1
                    else:
                        proposed_answer, answer_start = find_answer(paragraph['context'], answer['text'])
                        if (proposed_answer == answer['text'] ):
                            valid_answers += 1
                        if not only_count:
                            answer['text'] = proposed_answer
                            if answer_start >= 0:
                                answer['answer_start'] = answer_start
        print(str(valid_answers/answers))
        new_data.append(article)

    print("Number of answers: ", answers)
    print("Number of valid answers: ", valid_answers)
    print("Ratio of valid:", valid_answers / answers)
    if not only_count:
        new_data = {
            'data': new_data,
            'version': "1.1"
        }
        with open(filename[:-5] + "_fixed_answers.json", 'w') as fp:
            json.dump(new_data, fp)

def main():
    args = parser.parse_args()
    fix_answers(args.input) # to only show number of valid answers
    fix_answers_parallel(args.input)
    fix_answers(args.input) # to show number of valid answers

if __name__ == "__main__":
    main()
