#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import string
from html.parser import HTMLParser
import mysql.connector
import sys
import os


base_url = 'http://www.biquge.com.tw'


class Hot_article(object):
    __slots__ = ('article_id','title','author','abstract','link','image_link','status')


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


def get_html(url):
    r = BeautifulSoup(requests.get(url=url).content, 'html.parser')
    # req = urllib.request.Request(url)
    # with urllib.request.urlopen(req) as page:
    #     html = page.read()
    #     content = html.decode('utf8')
    content = str(r)

    return content


def get_hot_article_list(html):
    hot_list = []
    hot_reg = r'<div id="hotcontent">(.*)<div class="r">\s*<h2>公告牌</h2>'
    # .*? - 非贪婪匹配
    item_reg = r'<div class="item">.*?<div class="clear"></div>'

    hot_result = re.search(hot_reg, html, re.DOTALL)
    hot_html = hot_result.group(1).strip()

    hot_list = re.findall(item_reg, hot_html, re.DOTALL)
    return hot_list

def process_html(content):
    html_parser = HTMLParser()
    reuslt = html_parser.unescape(content)
    return reuslt



def parse_hot_articles(hot_list):
    results = []
    for item in hot_list:
        title_author_link_reg = r'<dt><span>(.*?)</span><a href="(.*?)">(.*?)</a></dt>'
        image_link_reg = r'<div class="image"><a href="(.*?)"><img alt=.*? src="(.*?)"'
        abstract_reg = r'<dd>(.*?)</dd>'

        title_author_link_result = re.search(title_author_link_reg,item)
        image_link_result = re.search(image_link_reg, item)
        abstract_result = re.search(abstract_reg, item, re.DOTALL)

        title = title_author_link_result.group(3)
        author = title_author_link_result.group(1)
        link = title_author_link_result.group(2)

        image_link = image_link_result.group(2)
        abstract = abstract_result.group(1)

        id_reg = r'http://www.biquge.com.tw/(.*?)/'
        id_result = re.search(id_reg, link)
        id = id_result.group(1)


        info = Hot_article()
        info.title = title
        info.author = author
        info.link = link
        info.image_link = image_link
        info.article_id = id
        info.abstract = process_html(abstract)
        results.append(info)

    return results


def save_hot_article_list_data(hot_list):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''insert into c_article_list(title, author, link, image_link, article_id, article_abstract, article_type)
              values (%s, %s, %s, %s, %s, %s, %s)'''

    for info in hot_list:
        status = check_id_from_db(info)
        if status :
            print("存在")
        else:
            cursor.execute(sql,
                           [info.title, info.author, info.link, info.image_link, info.article_id, info.abstract, '热门'])
            update_article_status(info.article_id)
    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()

# 检查是否存在这个小说链接
def check_id_from_db(info):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = '''select status from c_article_list where article_id = %s'''
    cursor.execute(sql, [info.article_id])
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    status = ''
    for item in values:
        status = item[0]

    return status

# 更新信息
def update_article_status(id):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'update c_article_list set status = 1 where article_id = %s'
    cursor.execute(sql, [id])
    conn.commit()
    cursor.close()
    conn.close()

def do_work():
    content = get_html(base_url)
    if content:
        hot_list = get_hot_article_list(content)
        all_hot_list = parse_hot_articles(hot_list)
        save_hot_article_list_data(all_hot_list)

if __name__=='__main__':
    do_work()
    print('02_articlt_list.py done')


