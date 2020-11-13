# -*- coding: utf-8 -*-
import json
from math import floor
import os


def combine_json_files(fnames):
    '''
    Assumes json files are in SQuAD format, i.e see https://github.com/facebookresearch/DrQA#format-b
    fnames is an array of filenames
    ''' 
    combined_data = []
    for fname in fnames:
        with open(fname) as f:
            data = json.load(f)['data']
        for article in data:
            combined_data.append(article)

    combined_data = {
        'data': combined_data,
        'version': "1.1"
    }
    with open("turk_combined_all.json",'w') as f:
        json.dump(combined_data,f)


def train_dev_test_split(filename, ratio_train=0.8, ratio_dev = 0.1):
    with open(filename) as f:
        dataset = json.load(f)['data']
    data_train = []
    data_dev = []
    data_test = []
    last_train_index = floor(len(dataset) * ratio_train)
    last_dev_index = floor(len(dataset) * (ratio_train + ratio_dev))
    i = 0
    for article in dataset:
        if i >= last_dev_index:
            data_test.append(article)
        elif i >= last_train_index:
            data_dev.append(article)
        else:
            data_train.append(article)
        i += 1

    data_train = {
        'data': data_train,
        'version': "1.1"
    }
    data_dev = {
        'data': data_dev,
        'version': "1.1"
    }
    data_test = {
        'data': data_test,
        'version': "1.1"
    }
    with open(filename[:-5]+"train.json", 'w') as fp:
        json.dump(data_train, fp)
    with open(filename[:-5]+"dev.json", 'w') as fp:
        json.dump(data_dev, fp)
    with open(filename[:-5]+"test.json", 'w') as fp:
        json.dump(data_test, fp)




def train_test_split(filename, ratio_train=0.8):
    with open(filename) as f:
        dataset = json.load(f)['data']
    data_train = []
    data_test = []
    last_train_index = floor(len(dataset) * ratio_train)
    i = 0
    for article in dataset:
        if i >= last_train_index:
            data_test.append(article)
        else:
            data_train.append(article)
        i += 1

    data_train = {
        'data': data_train,
        'version': "1.1"
    }
    data_test = {
        'data': data_test,
        'version': "1.1"
    }
    with open(filename[:-5]+"train.json", 'w') as fp:
        json.dump(data_train, fp)
    with open(filename[:-5]+"test.json", 'w') as fp:
        json.dump(data_test, fp)



