# -*- coding: utf-8 -*-
import json
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data-dir', help='Path of dataset to view', required=True)
parser.add_argument('-v', '--view_all', help='To view all of the datasets', required=False)


def view_data(file_name, view_questions=False, view_all_paragraphs=False):
    total_pars = 0
    total_quests = 0
    with open(file_name) as f:
        dataset = json.load(f)['data']
    articles = 0
    for article in dataset:
        articles += 1
        print("######################################################")
        print("######################################################")
        print("######################################################")
        print("Article:")
        print(article['title'])
        viewed_first = False  # For just viewing first paragraph
        for paragraph in article['paragraphs']:
            total_pars += 1
            if (not viewed_first or view_all_paragraphs):
                print("######################################################")
                print("Paragraph:")
                print(paragraph['context'])
                viewed_first = True
            for qa in paragraph['qas']:
                total_quests += 1
                if view_questions:
                    print("###########################")
                    print("Question:")
                    print(qa['question'])
                    print("###########################")
                    print("Answers:")
                for answer in qa['answers']:
                    if view_questions:
                        print(answer['text'])
    print("Number of articles: ", articles)
    print("Number of paragraphs: ", total_pars)
    print("Number of questions: ", total_quests)

def main():
    args = parser.parse_args()
    view_all = False
    if args.view_all == "1":
        view_all = True
    view_data(args.data_dir, view_all, view_all)

if __name__ == "__main__":
    main()

