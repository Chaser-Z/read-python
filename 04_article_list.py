#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import mysql.connector
from bs4 import BeautifulSoup
import requests
import re
import sys
import os

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


class Article(object):
    __slots__ = ('article_id','title','author','abstract','image_link')

    def __init__(self):
        self.title = None
        self.article_id = None
        self.image_link = None
        self.author = None
        self.abstract = None


# 从数据库中获取没有被抓取过的小说链接
def get_article_line_from_db():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'select link from c_article_list where status = 0 or status = 2'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    article_list = []
    for item in values:
        article_list.append(item[0])

    return article_list


# 获取h5内容
def get_html(url):
    r = BeautifulSoup(requests.get(url=url, verify=False).content, 'html.parser')
    content = str(r)

    return content

# 获取章节目录
def get_article_directory(html):

    article_title_reg = r'<meta content="(.*?)" property="og:novel:book_name"/>'
    article_author_reg = r'<meta content="(.*?)" property="og:novel:author"/>'
    article_abstract_reg = r'property="og:title"/>.*?<meta content="(.*?)" property="og:description"/>'
    article_image_link_reg = r'<meta content="(.*?)" property="og:image"/>'
    article_id_reg = r'<meta content="http://www.biquge.com.tw/(.*?)/" property="og:url"/'

    title_result = re.search(article_title_reg, html)
    author_result = re.search(article_author_reg, html)
    abstract_result = re.search(article_abstract_reg, html, re.DOTALL)
    image_link_result = re.search(article_image_link_reg, html)
    article_id_result = re.search(article_id_reg, html)

    article = Article()
    article.article_id =  article_id_result.group(1)
    article.title = title_result.group(1)
    article.author = author_result.group(1)
    article.abstract = abstract_result.group(1)
    article.image_link = image_link_result.group(1)

    return article


# 存入到数据库
def save_article_to_db(info, link):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''update c_article_list set article_id = %s, title = %s, author = %s, image_link = %s, article_abstract = %s where link = %s'''
    cursor.execute(sql,
                   [info.article_id, info.title, info.author, info.image_link, info.abstract, link])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()

# 更新信息
def update_article_status(id):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'update c_article_list set status = 1 where article_id = %s and status = 0'
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()

# 检查是否存在这个小说链接
def check_id_from_db(link):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = '''select status from c_article_list where link = %s'''
    cursor.execute(sql, [link])
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    status = ''
    for item in values:
        status = item[0]

    return status

def dowork():

    article_list = get_article_line_from_db()

    for link in article_list:
        status = check_id_from_db(link)
        if status != 1:
            html = get_html(link)
            article = get_article_directory(html)
            print('正在存储:', article.title)
            save_article_to_db(article, link)
            update_article_status(article.article_id)



if __name__ == '__main__':
    dowork()
    print('04_article_list done')