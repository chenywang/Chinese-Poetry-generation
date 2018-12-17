# -*- coding:utf-8 -*-
import re


def is_cn_char(ch):
    """ Test if a char is a Chinese character. """
    ch = to_unicode(ch)
    return isinstance(ch, unicode) and u'\u4e00' <= ch <= u'\u9fa5'


def is_cn_sentence(sentence):
    """ Test if a sentence is made of Chinese characters. """
    for ch in sentence:
        if not is_cn_char(ch):
            return False
    return True


def cleaning(text):
    text = to_str(text)
    text = text.lower()  # 小写
    text = text.replace('\r\n', " ")  # 新行，我们是不需要的
    text = text.replace('\n', " ")  # 新行，我们是不需要的
    text = text.replace('\r', " ")  # 新行，我们是不需要的
    text = text.replace('【', ".")  # 删除
    text = text.replace('】', ".")  # 删除
    text = re.sub(r"-", " ", text)  # 把 "-" 的两个单词，分开。（比如：july-edu ==> july edu）
    text = re.sub('，', ',', text)  #
    text = re.sub('。', '.', text)  #
    text = re.sub('！', '!', text)  #
    text = re.sub('？', '?', text)  #
    return text


def split_sentences(text):
    """ Split a piece of text into a list of sentences. """
    sentences = []
    i = 0
    for j in range(len(text) + 1):
        if j == len(text) or \
                text[j] in [u'，', u'。', u'！', u'？', u'、', u'\n']:
            if i < j:
                sentence = u''.join(filter(is_cn_char, text[i:j]))
                sentences.append(sentence)
            i = j + 1
    return sentences


def get_sentences_from_paragraph(para):
    para = cleaning(para)

    sentences = re.split(r"[,.?!]", str(para))

    # 只保留中英文的句子
    sentences = [filter_not_chinese_or_english(sentence) for sentence in sentences]

    # 去除空句子
    sentences = filter(lambda x: len(x) != 0, sentences)

    # 转化成unicode
    sentences = [to_unicode(sentence) for sentence in sentences]

    return sentences


def has_unknown(sentence, d):
    for word in sentence:
        if word == u' ':
            continue
        elif word not in d:
            return True
    return False


def filter_not_chinese_or_english(text):
    text = to_unicode(text)
    text = re.sub(u'[^\u4e00-\u9fa5\u0041-\u005a\u0061-\u007a]', u'', text)
    return to_str(text)


def to_unicode(s):
    return s.decode('utf-8') if isinstance(s, str) else s


def to_str(s):
    return s.encode('utf-8') if isinstance(s, unicode) else s


NUM_OF_SENTENCES = 4
CHAR_VEC_DIM = 512
