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
    __slots__ = ('title',	'update_status', 'last_update_date', 'last_update_directory', 'article_directory_list', 'article_directory_link_list', 'status')

    def __init__(self):
        self.title = None
        self.update_status = None
        self.last_update_date = None
        self.last_update_directory = None
        self.article_directory_list = None
        self.article_directory_link_list = None
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

    title_result = re.search(title_reg, article_directory_nav_result)
    last_update_date_result = re.search(last_update_date_reg, article_directory_nav_result)
    last_update_directory_result = re.search(last_update_directory_reg, article_directory_nav_result)

    article_directory_list_href_result = re.findall(article_directory_list_href_reg, article_directory_result, re.DOTALL)

    # 状态
    update_status = update_status_result.group(1)
    # 小说名字
    title = title_result.group(1)
    # 最近更新时间
    last_update_date = last_update_date_result.group(1)
    # 最近更新目录
    last_update_directory = last_update_directory_result.group(2)

    # 小说列表list
    article_directory_list = []
    # 小说浏览章节h5 list
    article_directory_link_list = []

    for index in article_directory_list_href_result:
        article_directory_list_result = re.search(article_directory_list_reg, index)
        article_directory_link_list.append(article_directory_list_result.group(1))
        article_directory_list.append(article_directory_list_result.group(2))
    info = Article_directory()
    info.title = title
    info.update_status = update_status
    info.last_update_directory = last_update_directory
    info.last_update_date = last_update_date
    info.article_directory_list = article_directory_list
    info.article_directory_link_list = article_directory_link_list
    return info


# 储存更新信息
def save_article_update_info_data(info):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''insert into c_article_update_info(title, update_status, last_update_date, last_update_directory) values (%s, %s, %s, %s)'''
    cursor.execute(sql, [info.title, info.update_status, info.last_update_date, info.last_update_directory])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()
# 储存章节列表
def save_article_directory_list_data(info):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = '''insert into c_article_directory_list(airicle_directory, article_directory_link)  values (%s, %s)'''
    for i in range(len(info.article_directory_list)):
        cursor.execute(sql, [info.article_directory_list[i], info.article_directory_link_list[i]])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()

def dowork():

    article_list = get_article_line_from_db()

    for link in article_list:
        html = get_html(link)
        info = get_article_directory(html)

        save_article_directory_list_data(info)
        save_article_update_info_data(info)


if __name__ == '__main__':
    dowork()
    print('15_article_directory_list done')