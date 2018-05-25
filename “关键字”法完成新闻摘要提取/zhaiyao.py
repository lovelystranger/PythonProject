import nltk

# 下面这两个包，需要在 PyCharm的Terminal中下载一下，在 python3交互界面下运行
# >>> import nltk
# >>> nltk.download('stopwords')
# >>> nltk.download('punkt')、
# 这样就会安装好了，然后 stopwords 和 punkt 就可以在 Pycharm 中使用了。

#  nltk.tokenize 是NLTK提供的分词工具包。所谓的分词 (tokenize) 实际就是把段落分成句子，把句子分成一个个单词的过程。
#  sent_tokenize() 函数对应的是分段为句。 word_tokenize()函数对应的是分句为词。
from nltk.tokenize import sent_tokenize, word_tokenize

# stopwords 是一个列表，包含了英文中那些频繁出现的词，如am, is, are。
from nltk.corpus import stopwords

# defaultdict 是一个带有默认值的字典容器。
from collections import defaultdict

# punctuation 是一个列表，包含了英文中的标点和符号。
from string import punctuation

# nlargest() 函数可以很快地求出一个容器中最大的n个数字。
from heapq import nlargest


stopwords = set(stopwords.words('english') + list(punctuation))
max_cut = 0.9
min_cut = 0.1

"""
计算出每个次出现的频率
word_sent 是一个已经分好词的列表
返回一个词典 freq[]
freq[w]代表了w出现的频率
"""


def compute_frequencies(word_sent):

    """
    :param word_sent:
    :return: freq[]
    """

    # defaultdict 和普通的 dict 的区别是它可以设置 default 的值，默认类型 int，值 0
    freq = defaultdict(int)

    #统计每个词出现的频率
    for s in word_sent:
        for word in s:
            #注意 stopwords
            if word not in stopwords:
                freq[word] += 1

    #统计最高出现的频次 m
    m = float(max(freq.values()))
    #所有单词的词频除以 m
    for w in list(freq.keys()):
        freq[w] /= m
        if freq[w] >= max_cut or freq[w] <= min_cut:
            del freq[w]

    #最后返回的是
    # {key:单词，value：重要性}

    return freq


def summarize(text, n):
    """

    :param text: 输入的文本
    :param n: 摘要的句子
    :return: 包含摘要的列表

    """
    # 首先把句子分出来
    sents = sent_tokenize(text)
    assert n <= len(sents)

    # 然后再分词, s.lower(),把单词全部转化为小写,为什么用 s.lower(), 我问过老师，老师说因为 stopwords()里面都是小写字母，会对分词结果造成影响，所以先全部转化成小写。
    word_sent = [word_tokenize(s.lower()) for s in sents]

    # freq 是一个词和词重要性的字典
    freq = compute_frequencies(word_sent)
    # ranking 则是句子和句子重要性的词典
    ranking = defaultdict(int)
    for i, word in enumerate(word_sent):
        for w in word:
            if w in freq:
                ranking[i] += freq[w]
    sents_idx = rank(ranking, n)
    return [sents[j] for j in sents_idx]


"""
考虑到句子比较多的情况
用遍历的方式找最大的n个数比较慢
我们这里调用heapq中的函数
创建一个最小堆来完成这个功能
返回的是最小的n个数所在的位置
"""


def rank(ranking, n):

    return nlargest(n, ranking, key=ranking.get)
    # return nlargest(n, ranking, key=None)

if __name__ == '__main__':
    # 这里我在 Pycharm中建立一个叫“NewSummary 的文件夹，所有有关 的文件我都放在这个目录里了
    with open("E:/Python/news.txt", "r") as myFile:
        text = myFile.read().replace('\n', '')
    res = summarize(text, 2)
    # 把内容放进一个 summary.txt 文件当中
    f = open("E:/Python/summary.txt", "w")
    for i in range(len(res)):
        print(res[i])
        f.write(res[i] + '\n')
    f.close()