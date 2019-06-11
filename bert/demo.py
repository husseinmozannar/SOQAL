#!/usr/bin/env python
# coding=utf-8

import tensorflow as tf
import bottle
from bottle import route, run
import threading
import json
import numpy as np

from time import sleep
from Bert_model import BERT_model

'''
This file is taken and modified from R-Net by Minsangkim142
https://github.com/minsangkim142/R-net
'''

app = bottle.Bottle()
query = ("", "")
response = ""

@app.get("/")
def home():
    with open('demo.html', 'r') as fl:
        html = fl.read()
        return html

@app.post('/answer')
def answer():
    passage = bottle.request.json['passage']
    question = bottle.request.json['question']
    print("received question: {}".format(question))
    # if not passage or not question:
    #     exit()
    global query, response
    query = (passage, question)
    if query[1] != "" and query[0] != "":
        while not response:
            sleep(0.1)
    else :
        response = "Paragraph or question field is empty"
    print("received response: {}".format(response))
    response_ = {"answer": response} 
    response = []
    return response_

class Demo(object):
    def __init__(self, model, config):
        run_event = threading.Event()
        run_event.set()
        self.close_thread = True
        self.model = model
        threading.Thread(target=self.demo_backend).start()
        app.run(port=8000, host='0.0.0.0')
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
            if query[1] != "" and query[0] != "":
                print("Hello")
                response = self.model.predict_example(query[0], query[1])
                query = ("", "")


import  argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='Path to bert_config.json', required=True)
parser.add_argument('-v', '--vocab', help='Path to vocab.txt', required=True)
parser.add_argument('-o', '--output', help='Directory of model outputs', required=True)

def main():
    args = parser.parse_args()
    AI = BERT_model(args.config, args.vocab, args.output)
    demo = Demo(AI, None)

if __name__ == "__main__":
    main()