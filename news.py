import requests
import re
import time
import urllib.request
import random
import csv


class spider(object):
    def __init__(self):
        print('Ready?')
        time.sleep(3)
        print('Go!')

    #获取网页源代码
    def getsoure(self,url):
        content = urllib.request.Request(url, headers={
            'Connection': 'keep-live',
            'Accept': 'text / html, application / xhtml + xml,q = 0.9, * / *',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        html = urllib.request.urlopen(content, timeout=10).read().decode('gb18030')
        return html

    def changepages(self,url,total_page):
        first_page = 'http://www.ict.edu.cn/news/n2/index.shtml'
        page_group=[]
        page_group.append(first_page)
        for i in range(2,total_page+1):
            link=re.sub(r'/n2/(index)\.shtml','/n2/%s.shtml'%i,url,re.S)
            page_group.append(link)
        return page_group

    def urls_in_one_page(self,html):
        urls = re.findall(r'<li><span>.*?<a href="(http://www.ict.edu.cn/news/n.*?)"',html, re.S)
        return urls

    def saveurls(self,url_list):
        f=open('urls.txt','a',encoding='utf-8')
        for i in url_list:
            f.writelines(i+'\n')
        f.close()

    #以下处理具体页面内容

    def get_news_from_page(self,url):
        newsdict={}
        page = urllib.request.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        html = urllib.request.urlopen(page,timeout=10).read().decode('gb18030')
        title = re.search('<title>(.*?)- 信息化动态 - 中国教育信息化网</title>',html,re.S).group(1)
        article = re.search('<div class="article">(.*?)<div class="share clearfix">', html, re.S).group(1)
        content = re.findall('>(.*?)<', article, re.S)
        content_string = ''.join(i.strip() for seq in content for i in seq) #哭，这个bug终于解决了！
        year = re.search('/n2/n(\d{4})',url,re.S).group(1)
        newsdict['年份'] = year
        newsdict['标题'] = title
        newsdict['新闻内容'] = content_string
        newsdict['链接'] = url
        return newsdict





if __name__=='__main__':

    eduinfo=spider()
    url_list=[]

    first_page = 'http://www.ict.edu.cn/news/n2/index.shtml'

    all_pages=eduinfo.changepages(first_page,311) #page=311


    for page in all_pages:
        print('正在爬取该页面的新闻链接：'+ page)
        try:
            html=eduinfo.getsoure(page)
        except:
            print('NO! Unaccessable...')
            time.sleep(5)
            continue
        links = eduinfo.urls_in_one_page(html)
        url_list.extend(links)
        time.sleep(random.randint(1, 10))

    print(len(url_list))
    with open('news_url.txt', 'a', encoding='utf-8') as f1:
        for url in url_list:
            f1.writelines(url+'\n')




    count=0
    total_news_info=[]

    for url in open('news_url.txt'):
        print('正在处理第%s条新闻： ' %count + url)
        try:
            news = eduinfo.get_news_from_page(url)
            count += 1
            total_news_info.append(news)
        except:
            print('ATTENTION! This is not available...')


        time.sleep(random.randint(1, 10))

    print('The number of unpacked url :', count)

    headers = ['年份', '标题', '新闻内容', '链接']


    with open('news_extend.csv', 'a', newline='',encoding='gb18030') as f2:
        f_csv = csv.DictWriter(f2, headers)
        f_csv.writeheader()
        f_csv.writerows(total_news_info)
        f2.close()
