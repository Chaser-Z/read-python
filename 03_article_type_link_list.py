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


class Type_article(object):
    __slots__ = ('link', 'article_type', 'status')


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


def process_html(content):
    html_parser = HTMLParser()
    reuslt = html_parser.unescape(content)
    return reuslt

# 获取type下的小说链接数组
def get_type_article_list(html, type):
    article_type_list = []
    type1_reg = r'<div id="newscontent">.*<div class="l">.*<h2>.*</h2>(.*?).?<div class="r">'
    # .*? - 非贪婪匹配
    type2_reg = r'<li><span class="s2">.?<a href=.*?</span></li>'

    type_result = re.search(type1_reg, html, re.DOTALL)
    type_html = type_result.group(1).strip()
    article_type_list = re.findall(type2_reg, type_html, re.DOTALL)

    results = []
    for item in article_type_list:
        item_reg = r'<li><span class="s2">.?<a href="(.*?)".*</span></li>'
        item_result = re.search(item_reg, item)

        info = Type_article()
        info.link = item_result.group(1)
        info.status = 0
        if type == 'xuanhuan':
            type = '玄幻'
        if type == 'xiuzhen':
            type = '修真'
        if type == 'dushi':
            type = '都市'
        if type == 'lishi':
            type = '历史'
        if type == 'wangyou':
            type = '网游'
        if type == 'kehuan':
            type = '科幻'
        if type == 'kongbu':
            type = '恐怖'
        if type == 'quanben':
            type = '全本'
            info.status = 2
        info.article_type = type
        results.append(info)
    return results


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

# 存入到数据库
def save_article_link_to_db(info):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''insert into c_article_list(link, article_type, status)
                  values (%s, %s, %s)'''

    cursor.execute(sql,
                   [info.link, info.article_type, info.status])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()


def do_work():
    type_list = ['xuanhuan', 'xiuzhen', 'dushi', 'lishi', 'wangyou', 'kehuan', 'kongbu', 'quanben']
    for type in type_list:
        url = base_url + '/' + type + '/'
        content = get_html(url)
        if content:
            article_type_list = get_type_article_list(content, type)
            for info in article_type_list:
                status = check_id_from_db(info.link)
                if status :
                    #print(type)
                    print('已经存在的link:', info.link)
                else:
                    print('抓取的link:', info.link)
                    save_article_link_to_db(info)

if __name__=='__main__':
    do_work()
    print('03_articlt_type_link_list.py done')


