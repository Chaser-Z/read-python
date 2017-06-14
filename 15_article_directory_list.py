#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import mysql.connector
from bs4 import BeautifulSoup
import requests
import re

def read_db_config():
    config = configparser.ConfigParser()
    config.read('db.cnf')
    host = config.get('mysql', 'host')
    port = config.get('mysql', 'port')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    return host, port, user, password, database

_host, _port, _user, _password, _database = read_db_config()


class Article_directory(object):
    __slots__ = ('title', 'article_id', 'image_link', 'author', 'update_status', 'last_update_date', 'last_update_directory', 'airicle_directory', 'article_directory_link', 'status')

    def __init__(self):
        self.title = None
        self.article_id = None
        self.image_link = None
        self.author = None
        self.update_status = None
        self.last_update_date = None
        self.last_update_directory = None
        self.airicle_directory = None
        self.article_directory_link = None
        self.status = None

# 从数据库中获取没有被抓取过的小说链接
def get_article_line_from_db():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'select link from c_article_hot_list where status = 0'
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
    r = BeautifulSoup(requests.get(url=url).content, 'html.parser')
    content = str(r)

    return content

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
        article_directory_link_list.append(article_directory_list_result.group(1))
        article_directory_list.append(article_directory_list_result.group(2))

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
        info.airicle_directory = article_directory_list[i]
        info.article_directory_link = article_directory_link_list[i]
        #info.status = 1
        infos.append(info)
        #update_article_status()

    return infos


# 储存更新信息
def save_article_detail(infos):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''insert into c_article_detail(title, article_id, update_status, last_update_date, last_update_directory, airicle_directory, article_directory_link) values (%s, %s, %s, %s, %s, %s, %s)'''

    for info in infos:
        cursor.execute(sql, [info.title, info.article_id, info.update_status, info.last_update_date, info.last_update_directory, info.airicle_directory, info.article_directory_link])
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


def dowork():

    article_list = get_article_line_from_db()

    for link in article_list:
        html = get_html(link)
        infos = get_article_directory(html)
        save_article_detail(infos)

        lens = len(infos)
        print('共', lens)
        for i in range(lens):
            update_article_status()
            print('第：', i + 1)

if __name__ == '__main__':
    dowork()
    print('15_article_directory_list done')