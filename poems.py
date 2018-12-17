#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from random import shuffle

import pandas as pd

from config import config
from paths import poems_path, check_uptodate
from singleton import Singleton
from utils import to_unicode, get_sentences_from_paragraph, has_unknown
from word_dict import WordDict


class Poems(Singleton):

    def __init__(self):
        if not check_uptodate(poems_path):
            self.__gen_poems()
        self.poems = []
        with open(poems_path, 'r') as fin:
            for line in fin.readlines():
                self.poems.append(line.strip().split())

    def __getitem__(self, index):
        if index < 0 or index >= len(self.poems):
            return None
        return self.poems[index]

    def __len__(self):
        return len(self.poems)

    def __iter__(self):
        return iter(self.poems)

    def shuffle(self):
        shuffle(self.poems)

    @staticmethod
    def __gen_poems():
        print("Parsing poems ...")
        word_dict = WordDict()

        for corpus in config.poem_corpus:
            df = pd.read_csv(corpus, sep='\t')
            df['sentences'] = df['body'].apply(get_sentences_from_paragraph)
            df['sentences'] = df['sentences'].apply(lambda ss: u' '.join(ss))
            # 删除包含未知字的诗句
            df['has_unknown'] = df['sentences'].apply(has_unknown, d=word_dict)
            df = df[df['has_unknown'] == False]
            df = df[['sentences']]
            df.to_csv(poems_path, index=False, header=True, sep='\t', encoding='utf-8')


# For testing purpose.
if __name__ == '__main__':
    poems = Poems()
    for i in range(10):
        print(u' '.join(poems[i]))
