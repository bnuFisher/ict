# -*- coding: UTF-8 -*-
#using python3.5
#used for 博士论文
import re
import time
import urllib.request
import random
import string
import csv


url_list=[] #博士论文url队列



def getpagecontent(url_list):
    count=0
    rows=[]
    miss_list=[]
    print('Ready?')
    time.sleep(3)
    print('Go!')
    for url in url_list:
        print('running url index%s' % count)
        try:
            html = urllib.request.urlopen(url,timeout=10).read().decode('utf-8')
        except:
            print('url index %s is not valid.' % count)
            miss_list.append(url)
            continue
        title = re.search('<h1 id="spanTitle"><span id="chTitle">(.*?)</span></h1>', html, re.S).group(1)
        author = re.search('【作者】.*?>(.*?)</a>', html, re.S).group(1).strip()
        tutor = re.search('【导师】.*?>(.*?)</a>', html, re.S).group(1).strip()
        university = re.search('【作者基本信息】.+?>(.*?)</a>', html, re.S).group(1)
        major_year_degree = re.search('【作者基本信息】.+?</a>，(.*?)</p>', html, re.S).group(1).strip()
        list1 = major_year_degree.strip().split('，')
        major = list1[0].strip(string.whitespace)
        year = list1[1].strip(string.whitespace)
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
        info['标题'] = title
        info['作者'] = author
        info['导师'] = tutor
        info['学校'] = university
        info['专业'] = major
        info['年份'] = year
        info['摘要'] = summary
        info['关键词'] = keyword
        info['被引频次'] = quoted
        info['下载频次'] = download
        count += 1
        rows.append(info)
        time.sleep(random.randint(4, 9))
    return rows,count



def writing(rows,count): #建议分批次爬去，分批次写入
    headers = ['标题', '作者', '学校', '专业', '导师', '年份', '摘要', '关键词', '被引频次', '下载频次']
    with open('doctor_info.csv', 'a', newline='', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader() #第二轮开始可以注释掉
        f_csv.writerows(rows)
        f.close()
    print('total pieces processed in this turn= %s'%count)



rows,count=getpagecontent(url_list)
writing(rows,count)
