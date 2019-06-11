# -*- coding: utf-8 -*-
import csv
import json
from random import randint
MAX_INT = 999999999999



def batch_to_json(fname):
    with open(fname, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, )
        initial_row = False
        worker = 0
        for row in csv_reader:
            if initial_row is True:
                initial_row = False
                continue
            if row['AssignmentStatus'] == "Approved":
                continue
            articles = []
            i = j = k = 0
            for i in range(1,6):
                article_title = row["Input.article"+str(i)]
                paragraphs = []
                for j in range(1,4):
                    paragraph_context = row['Input.paragraph'+str(i)+str(j)]
                    qas = []
                    for k in range(1,4):
                        id = str(randint(0, MAX_INT))
                        ques = row["Answer.question"+str(i)+str(j)+str(k)]
                        ans = row["Answer.answer"+str(i)+str(j)+str(k)]
                        answer_start = max(paragraph_context.find(ans), 0)
                        answer = {
                            'text': ans,
                            'answer_start': answer_start
                        }
                        question = {
                            'question': ques,
                            'id': id,
                            'answers': [answer]
                        }
                        qas.append(question)
                    paragraph = {
                        'context': paragraph_context,
                        'qas': qas
                    }
                    paragraphs.append(paragraph)
                article ={
                    'title': article_title,
                    'paragraphs': paragraphs
                }
                articles.append(article)
            with open(fname[:-4] + "_worker_" + str(worker) + ".json", 'w') as fp:
                json.dump(articles, fp)
            worker +=1
