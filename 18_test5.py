#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import threading
import urllib

import mysql.connector
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import random
import time
from urllib import request

mainURL = ''

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

def get_data(filename, default='') -> list:
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(os.path.dirname(__file__))
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data

def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(get_data('user_agents.txt', USER_AGENT))

headers = {'user-agent': get_random_user_agent()}


def current_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def read_db_config():
    current = current_file_dir()
    config = configparser.ConfigParser()
    config.read(os.path.join(current, 'db.cnf'))
    host = config.get('mysql', 'host')
    port = config.get('mysql', 'port')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    return host, port, user, password, database

_host, _port, _user, _password, _database = read_db_config()

class Article_directory(object):
    __slots__ = ('title', 'article_id', 'image_link', 'author', 'update_status', 'last_update_date', 'last_update_directory', 'article_directory', 'article_directory_link', 'status')

    def __init__(self):
        self.title = None
        self.article_id = None
        self.image_link = None
        self.author = None
        self.update_status = None
        self.last_update_date = None
        self.last_update_directory = None
        self.article_directory = None
        self.article_directory_link = None
        self.status = None

# 从数据库中获取没有被抓取过的小说链接
def get_article_line_from_db():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'select link from c_article_list where status = 1'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    article_list = []
    for item in values:
        article_list.append(item[0])

    return article_list


# 获取h5内容
def get_html(urls):

    def crawl_and_save(html):
        print('执行')
        infos = get_article_directory(html)
        save_article_detail(infos)


    def get(url):
        try:
            r = requests.get(url, timeout=120.0, headers=headers, verify=False, allow_redirects=True).content
        except:
            pass
        else:
            if r:
                r = BeautifulSoup(r, 'html.parser')
                content = str(r)
                if content:
                    crawl_and_save(content)

    t1 = time.time()
    number = 0
    th = []
    # 最大的并发数量
    maxthreads = 5

    for url in urls:
        number += 1
        t1 = threading.Thread(target=get, args=(url,))
        t1.start()
        th.append(t1)
        if number > maxthreads:
            [i.join() for i in th]
            number = 0
            th = []
    [i.join() for i in th]

    print(time.time() - t1)



# 获取章节目录
def get_article_directory(html):

    update_status_reg = r'<meta content="(.*?)" property="og:novel:status"/>'
    article_directory_nav_reg = r'<div class="box_con">(.*?)<div id="sidebar">'
    article_directory_reg = r'<div id="list">(.*?)<div id="footer" name="footer">'

    update_status_result = re.search(update_status_reg, html)
    article_directory_nav_result = re.findall(article_directory_nav_reg, html, re.DOTALL)[0]
    article_directory_result = re.findall(article_directory_reg, html, re.DOTALL)[0]

    title_reg = r'<h1>(.*?)</h1>'
    last_update_date_reg = r'<p>最后更新：(.*?)</p>'
    last_update_directory_reg = r'<p>最新章节：(.*?)>(.*?)</a></p>'

    article_directory_list_href_reg = r'<dd>(.*?)</dd>'
    article_directory_list_reg = r'<a href="(.*?)">(.*?)</a>'

    article_id_reg = r'<meta content="http://www.biquge.com.tw/(.*?)/" property="og:url"/'

    title_result = re.search(title_reg, article_directory_nav_result)
    last_update_date_result = re.search(last_update_date_reg, article_directory_nav_result)
    last_update_directory_result = re.search(last_update_directory_reg, article_directory_nav_result)

    article_directory_list_href_result = re.findall(article_directory_list_href_reg, article_directory_result, re.DOTALL)
    article_id_result = re.search(article_id_reg, html)

    # 小说列表list
    article_directory_list = []
    # 小说浏览章节h5 list
    article_directory_link_list = []

    for index in article_directory_list_href_result:
        article_directory_list_result = re.search(article_directory_list_reg, index)
        info = Article_directory()
        info.article_directory_link = article_directory_list_result.group(1)
        info.article_directory =  article_directory_list_result.group(2)
        # 存在这个信息就不储存
        ishave = check_chapter_id_from_db(info)
        if ishave == False:
            article_directory_link_list.append(article_directory_list_result.group(1))
            article_directory_list.append(article_directory_list_result.group(2))

    print('共需要抓取章数', len(article_directory_list))

    infos = []

    for i in range(len(article_directory_list)):

        # 状态
        update_status = update_status_result.group(1)
        # 小说名字
        title = title_result.group(1)
        # 最近更新时间
        last_update_date = last_update_date_result.group(1)
        # 最近更新目录
        last_update_directory = last_update_directory_result.group(2)
        # 文章id
        article_id = article_id_result.group(1)

        info = Article_directory()
        info.article_id =  article_id
        info.title = title
        info.update_status = update_status
        info.last_update_directory = last_update_directory
        info.last_update_date = last_update_date
        info.article_directory = article_directory_list[i]
        info.article_directory_link = article_directory_link_list[i]
        #info.status = 1
        infos.append(info)
        #update_article_status()
        update_article_status()
        print('已经抓取章节进度：', i + 1)

    return infos


# 储存更新信息
def save_article_detail(infos):

    for info in infos:
        # 存在这个信息就不储存
        ishave = check_chapter_id_from_db(info)
        if ishave == False:
            conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
            cursor = conn.cursor()
            sql = '''insert into c_article_detail(title, article_id, update_status, last_update_date, last_update_directory, article_directory, article_directory_link) values (%s, %s, %s, %s, %s, %s, %s)'''

            cursor.execute(sql, [info.title, info.article_id, info.update_status, info.last_update_date, info.last_update_directory, info.article_directory, info.article_directory_link])
            conn.commit()
            cursor.close()
            conn.close()
            conn.disconnect()

# 更新信息
def update_article_status():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'update c_article_detail set status = 1'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# 更新完结信息
def update_article_finish_status():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'update c_article_detail set status = 2'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

# 查看是否存在这个章节的id
def check_chapter_id_from_db(info):

    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'select article_directory_link = %s from c_article_detail where article_directory = %s'
    cursor.execute(sql, [info.article_directory_link, info.article_directory])
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return True if len(values) > 0 else False

def dowork():

    article_list = get_article_line_from_db()
    get_html(article_list)

if __name__ == '__main__':
    dowork()
    #print('15_article_directory_list done')
