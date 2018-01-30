#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     spider_mzitu
   Description :
   Author :       Nathan
   date：          2018/1/30
-------------------------------------------------
   Change Activity:
                   2018/1/30:
-------------------------------------------------
"""
__author__ = 'Nathan'
import requests
from bs4 import BeautifulSoup
import random
import os

class spdier(object):
    def __init__(self):
        self.url="http://www.mzitu.com/page/{pagenum}"
        self.user_agent_list=[ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


    def run(self):
        ##开始访问每一个主页面
        for i in range(1,4):
            headers = {'User-Agent': random.choice(self.user_agent_list), 'Referer': ''}
            html=requests.get(url=self.url.format(pagenum=str(i)),headers=headers)
            Soup=BeautifulSoup(html.text,'lxml')
            links=Soup.find('ul',id="pins").find_all('a')
            page_links=[]
            for link in links:
                page_links.append(link.get('href'))##获得每个主页面的链接
            for page in page_links:
                self.process_second_page(page)


    def process_second_page(self,link):
        ##处理次级页面
        headers = {'User-Agent': random.choice(self.user_agent_list), 'Referer': link}
        pagehtml = requests.get(url=link, headers=headers)
        pagehtml_Soup = BeautifulSoup(pagehtml.text, 'lxml')
        num_total_page=pagehtml_Soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
        self.download_pic(link,num_total_page)


    def download_pic(self,link,num):
        headers = {'User-Agent': random.choice(self.user_agent_list), 'Referer': link,'Connection':'Keep-Alive'}
        name=link.split('/')[-1]
        if(os.path.exists('./download/'+name)):
            print(name+'has download')
        else:
            os.mkdir('./download/'+name)
            for i in range(1,int(num)+1):
                url=link+'/'+str(i)
                html = requests.get(url=url,headers=headers)
                print('sucess get html')
                Soup=BeautifulSoup(html.text,'lxml')
                image_url=Soup.find('div',class_='main-image').find('img')['src']
                image=requests.get(url=image_url,headers=headers)
                with open('./'+name+'/'+str(i) + '.jpg', 'ab')as f:
                    f.write(image.content)

spdier=spdier()
spdier.run()