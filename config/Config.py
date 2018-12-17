# -*- coding:utf-8 -*-
# @Author : Michael-Wang

import os

PROJECT_PATH = os.path.abspath(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        os.pardir))


class Config(object):
    data_dir = 'data/'
    raw_dir = 'raw/'

    word_dict_corpus_list = ['qts_tab.txt', 'qss_tab.txt', 'qsc_tab.txt', 'qtais_tab.txt', 'yuan.all', 'ming.all',
                             'qing.all']
    word_dict_corpus_list = [raw_dir + corpus for corpus in word_dict_corpus_list]
    MAX_DICT_SIZE = 10000

    poem_corpus = ['ming.all']
    poem_corpus = [raw_dir + corpus for corpus in poem_corpus]
