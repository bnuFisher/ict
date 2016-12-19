# !/usr/bin/env python
# -*- coding: utf-8 -*-
#using python3.5
#used for 期刊论文
import re
import time
import urllib.request
import random
import string
import csv

url_list=[] #期刊url队列，建议分批次抓取，分批次写入

def getpagecontent(url_list):
    count=0
    rows=[]
    miss_list=[]
    key_journal={}
    print('Ready?')
    print('Go!')
    for url in url_list:
        try:
            print('running url... index: %s'%count)
        except:
            print('url: %s is not valid. '%url)
            miss_list.append(url)
            count += 1
            time.sleep(random.randint(3, 5))
            continue

        html = urllib.request.urlopen(url,timeout=20).read().decode('utf-8')
        title = re.search('<h1 id="spanTitle"><span id="chTitle">(.*?)</span></h1>', html, re.S).group(1)
        author = re.search('【作者】.*?>(.*?)</a>', html, re.S).group(1).strip()
        institution = re.search('【机构】.+?>(.*?)</a>', html, re.S).group(1)
        info_block=re.search('<div class="detailLink">(.*?)<span id="mlyll">',html,re.S).group(1)
        info_base = re.findall('<a onclick=.*?CJFQbaseinfo.*?>(.*?)</a>', info_block, re.S)
        title_journal = info_base[0]
        year = re.search('<a onclick=.*?CJFQyearinfo.*?>(.*?)</a>', info_block, re.S).group(1).strip()
        summary = re.search('<span id="ChDivSummary" name="ChDivSummary">(.*?)</span>', html, re.S).group(1).strip()
        total_keyword = re.search('<span id="ChDivKeyWord" name="ChDivKeyWord">(.*?)</span>', html, re.S).group(1)
        keyword = re.findall('<a class.*?>(.*?)</a>', total_keyword, re.S)

        if re.search('【被引频次】(.*?)</li>', html, re.S) == None:
            quoted = 0
        else:
            quoted = re.search('【被引频次】(.*?)</li>', html, re.S).group(1)
        if re.search('【下载频次】(.*?)</li>', html, re.S) == None:
            download = 0
        else:
            download = re.search('【下载频次】(.*?)</li>', html, re.S).group(1)
        info = {}
        if title_journal in key_journal:
            info['是否核心期刊']=key_journal[title_journal]
        else:
            try:
                journal_abbr = re.search("[^\"]mailto:(.*?)@", html, re.S).group(1)
                journal_url = 'http://navi.cnki.net/knavi/journal/Detailq/CJFQ/' + journal_abbr + '?Year=&Issue=&Entry=&uid='
                time.sleep(random.randint(3, 5))
                html_journal = urllib.request.urlopen(journal_url, timeout=20).read().decode('utf-8')
                if re.search('<p class="journalType">', html_journal, re.S) != None:
                    key_journal[title_journal] = '是'
                    info['是否核心期刊'] = key_journal[title_journal]
                else:
                    key_journal[title_journal] = '否'
                    info['是否核心期刊'] = key_journal[title_journal]
            except:
                info['是否核心期刊']='期刊信息缺失'

        info['标题'] = title
        info['第一作者'] = author
        info['作者单位'] = institution
        info['刊物'] =title_journal
        info['发表时间'] = year
        info['摘要'] = summary
        info['关键词'] = keyword
        info['被引频次'] = quoted
        info['下载频次'] = download
        count += 1
        rows.append(info)
        time.sleep(random.randint(3, 5))

    return rows,count




def writing(rows,count):

    headers = ['标题','摘要', '关键词', '第一作者', '作者单位', '刊物', '是否核心期刊','发表时间','被引频次', '下载频次']
    with open('journal_info.csv', 'a', newline='', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
        f.close()  #一轮过后可以注释掉
    print('total pieces processed in this turn= %s'%count)



rows,count=getpagecontent(url_list)
writing(rows,count)



