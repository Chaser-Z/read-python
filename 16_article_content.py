#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import configparser
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from html.parser import HTMLParser
import random
import time
import sys
import os

base_url = 'http://www.biquge.com.tw'


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


class Article_content(object):
    __slots__ = ('content', 'status')

    def __init__(self):
        self.content = None
        self.status = None



# 获取内容那段h5
def get_content_html(url):
    url = base_url + url
    r = BeautifulSoup(requests.get(url=url, verify=False).content, 'html.parser')
    content_reg = r'<div class="content_read">(.*?)<div class="footer">'
    content = str(re.findall(content_reg, str(r), re.DOTALL))

    return content
# 从数据库中获取link
def get_directory_link_list_from_db():

    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = 'select article_directory_link from c_article_detail where content is NULL'
    cursor.execute(sql)
    values = cursor.fetchall()

    article_directory_link_list = []

    for item in values:
        article_directory_link_list.append(item[0])

    return article_directory_link_list


def process_html(content):
    html_parser = HTMLParser()
    result = html_parser.unescape(content)
    return result


# 给Article_content 赋值
def get_article_content(html):

    content_reg = r'<div id="content">(.*?)</div>'

    content_result = re.search(content_reg, html, re.DOTALL)

    content = content_result.group(1)

    content = content.replace(r'\xa0\xa0\xa0\xa0', '  ')
    content = content.replace(r'<br/>\n<br/>\r\n', '\n')

    info = Article_content()
    info.content = process_html(content)
    print(info.content)
    return info


# 存到数据库中
def save_article_content_data(info, link):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql =  'update c_article_detail set content = %s where article_directory_link = %s'
    cursor.execute(sql, [info.content, link])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()



def dowork():
    article_directory_link_list = get_directory_link_list_from_db()
    total_num = len(article_directory_link_list)
    print('需要下载章节数:', total_num)
    if article_directory_link_list:
        for index,item in enumerate(article_directory_link_list):
            content = get_content_html(item)
            info = get_article_content(content)
            print('已经下载第',index)
            # interval = random.uniform(1, 3)
            # time.sleep(interval)
            save_article_content_data(info, item)


if __name__ == '__main__':
    dowork()
    print('16_article_content.py done')

