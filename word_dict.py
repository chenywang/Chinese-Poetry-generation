# -*- coding:utf-8 -*-
import pandas as pd

from config import config
from paths import char_dict_path, check_uptodate
from singleton import Singleton
from utils import is_cn_char, to_unicode


def start_of_sentence():
    return u'^'


def end_of_sentence():
    return u'$'


class WordDict(Singleton):

    def __init__(self):
        if not check_uptodate(char_dict_path):
            self.__gen_char_dict()
        self._int2char = list()
        self._char2int = dict()

        df = pd.read_csv(char_dict_path)
        for index, row in df.iterrows():
            word = to_unicode(row['word'])
            self._char2int[word] = index + 1
            self._int2char.append(word)
        # 添加开头标记和结尾标记
        self._int2char.insert(0, start_of_sentence())
        self._int2char.append(end_of_sentence())
        self._char2int[start_of_sentence()] = 0
        self._char2int[end_of_sentence()] = len(self._int2char) - 1

    def char2int(self, ch):
        if ch not in self._char2int:
            return -1
        return self._char2int[ch]

    def int2char(self, idx):
        return self._int2char[idx]

    def __len__(self):
        return len(self._int2char)

    def __iter__(self):
        return iter(self._int2char)

    def __contains__(self, ch):
        return ch in self._char2int

    @staticmethod
    def __gen_char_dict():
        print "Generating dictionary from corpus ..."
        # Count char frequencies.
        chinese_word_dict = dict()
        for corpus in config.corpus_list:
            with open(corpus, 'r') as corpus_file:
                for line in corpus_file.readlines():
                    line = to_unicode(line)
                    for word in line:
                        if is_cn_char(word):
                            chinese_word_dict.setdefault(word, 0)
                            chinese_word_dict[word] += 1
        # Sort in decreasing order of frequency.
        word_count_list = sorted(chinese_word_dict.items(), key=lambda x: x[1], reverse=True)[:config.MAX_DICT_SIZE]
        df = pd.DataFrame(word_count_list, columns=['word', 'count'])
        df.to_csv(char_dict_path, header=True, index=False, encoding='utf-8')


# For testing purpose.
if __name__ == '__main__':
    char_dict = WordDict()
    for i in range(10):
        ch = char_dict.int2char(i)
        print(ch)
        assert i == char_dict.char2int(ch)
