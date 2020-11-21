#!/usr/bin/env python
# coding=utf-8

import tensorflow as tf
import bottle
from bottle import route, run, static_file
import threading
import numpy as np
import os
from soqal import SOQAL
from time import sleep
import sys
import pickle
sys.path.append(os.path.abspath("retriever"))
from retriever.GoogleSearchRetriever import ApiGoogleSearchRetriever
from retriever.TfidfRetriever import HierarchicalTfidf
from retriever.TfidfRetriever import TfidfRetriever
sys.path.append(os.path.abspath("bert"))
from bert.Bert_model import BERT_model
'''
This file is taken and modified from R-Net by Minsangkim142
https://github.com/minsangkim142/R-net
'''

app = bottle.Bottle()
query = []
response = ""
my_module = os.path.abspath(__file__)
parent_dir = os.path.dirname(my_module)
static_dir = os.path.join(parent_dir, 'static')

@app.get("/")
def home():
    with open('demo_open.html', encoding='utf-8') as fl:
        html = fl.read()
        return html

@app.get('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=static_dir)

@app.post('/answer')
def answer():
    question = bottle.request.json['question']
    print("received question: {}".format(question))
    # if not passage or not question:
    #     exit()
    global query, response
    query = question
    if query != "":
        while not response:
            sleep(0.1)
    else:
        response = "Please write a question"
    print("received response: {}".format(response))
    response_ = {"answer": response} 
    response = []
    return response_

class Demo(object):
    def __init__(self, model, config):
        self.model = model
        run_event = threading.Event()
        run_event.set()
        self.close_thread = True
        threading.Thread(target=self.demo_backend).start()
        app.run(port=9999, host='0.0.0.0')
        try:
            while 1:
                sleep(.1)
        except KeyboardInterrupt:
            print("Closing server...")
            self.close_thread = False
    def demo_backend(self):
        global query, response
        while self.close_thread:
            sleep(0.1)
            if query:
                response = self.model.ask(query)
                query = []

import  argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='Path to bert_config.json', required=True)
parser.add_argument('-v', '--vocab', help='Path to vocab.txt', required=True)
parser.add_argument('-o', '--output', help='Directory of model outputs', required=True)
parser.add_argument('-r', '--ret-path', help='Retriever Path', required=True)


def main():
    args = parser.parse_args()
    base_r = pickle.load(open(args.ret_path, "rb"))
    ret = HierarchicalTfidf(base_r, 50, 50)
    red = BERT_model(args.config, args.vocab, args.output)
    AI = SOQAL(ret, red, 0.999)
    demo = Demo(AI, None)

if __name__ == "__main__":
    main()