# !/usr/bin/env python
# -*- coding: utf-8 -*-
#using python3.5
#以对新闻文本的分词为例进行说明
import re
import jieba
import jieba.analyse
import time
from gensim.models import word2vec as word
import logging




jieba.load_userdict("userdict.txt")
jieba.analyse.set_stop_words("stop_words.txt")


def keywords_news(file1,file2,year=2016):
    dic = {}
    list1 = []
    print('running...')
    count=0
    for line in open(file1,encoding='utf-8'):
        if len(line)>0:
            count +=1
            keys=[]
            tags = jieba.analyse.extract_tags(line.strip(),withWeight=False,topK=10)
            for i in tags:
                if re.search('[每所附这第届国省州市区县镇 \
                       李张陈王赵钱孙周陆刘徐许朱沈苏俞顾贾胡吴霍谢郑孙杨柳侯黄林何马郭罗梁宋唐冯于董萧曹蔡袁邓卢丁宁叶颜静伟锋毛翁戴蒋蓉凯曾傅明波钟春秦 \
                       魏吕瞿谭邱石范田易方夏汪赖江庄鲍游翁军温萍龙宝奇闵莉陶杰雨孟牛剑阳康梅谈费姚葛皇武该洪甘十韩昌凌东涛鲁哥俊骏君潘邹彭鹏雪峰隆兰耀尤邢孔包宏桥南北皖 \
                       京津沪杭浙粤辽吉赣陇港澳湾珠了我你他她它]',i) == None: #即使有停用词表，一些人名、地名和虚词仍然不能准确地被过滤，因此我加了一重过滤
                    keys.append(i.strip())
            lis=keys[:6]
            for i in lis:
                if i not in dic:
                    dic[i]=1
                else:
                    dic[i] += 1

    for key,val in dic.items():
        list1.append((val,key))

    list1.sort(reverse=True)

    print('Total num of news processed:',count)


    with open(file2,'a',encoding='gb18030') as f2:
        f2.writelines('keywords_%s\n'%str(year))
        for i in list1[:20]: #保留前30位高频关键词
            i=str(i)
            f2.writelines(i)
            f2.writelines('\n')


# keywords_news('news_2010.txt', 'keywords_all.csv', 2010) #将新闻按年份保存，分别提取各年度的关键词
# keywords_news('news_2011.txt', 'keywords_all.csv', 2011)
# keywords_news('news_2012.txt', 'keywords_all.csv', 2012)
# keywords_news('news_2013.txt', 'keywords_all.csv', 2013)
# keywords_news('news_2014.txt', 'keywords_all.csv', 2014)
# keywords_news('news_2015.txt', 'keywords_all.csv', 2015)
# keywords_news('news_2016.txt', 'keywords_all.csv', 2016)

# keywords_news('news_all.txt', 'keywords_all.csv') # 全部新闻一起


def cut_news(file): #file=news_all.txt
    list_news=[]
    print('running...')
    for line in open(file,encoding='utf-8'):
        if len(line)>1:
            line=' '.join(jieba.cut(line,cut_all=False))
            list_news.append(line)
    yield list_news


# t=cut_news('news_all.txt')



def news_cut_into_file(list_news,file3):
    with open(file3, 'a', encoding='utf-8') as f3:
        for line in list_news:
            f3.writelines(line)



# news_cut_into_file(t,'news_cut.txt')



#以下词向量训练及相关词计算

# sentences = word.Text8Corpus('news_cut.txt')  # 加载语料，
# model = word.Word2Vec(sentences, size=300)  #进行词向量训练,时间取决于语料量

# words = model.most_similar("智慧教育", topn=20)  #举例，计算“智慧教育”的相关词

# for i in words:
#     print(i[0],i[1])

