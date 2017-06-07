#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import configparser
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from html.parser import HTMLParser


base_url = 'http://www.biquge.com.tw'


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


class Article_content(object):
    __slots__ = ('title', 'content', 'status')

    def __init__(self):
        self.title = None
        self.content = None
        self.status = None



# 获取内容那段h5
def get_content_html(url):
    url = base_url + url
    r = BeautifulSoup(requests.get(url=url).content, 'html.parser')

    content_reg = r'<div class="content_read">(.*?)<div class="footer">'
    content = str(re.findall(content_reg, str(r), re.DOTALL))

    return content
# 从数据库中获取link
def get_directory_link_list_from_db():

    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = 'select article_directory_link from c_article_directory_list where status = 0'
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

    title_reg = r'<a href="(http://.*?)">(.*?)</a>'
    content_reg = r'<div id="content">(.*?)</div>'

    title_result = re.search(title_reg, html)
    content_result = re.search(content_reg, html, re.DOTALL)

    title = title_result.group(2)
    content = content_result.group(1)


    info = Article_content()
    info.title = title
    info.content = process_html(content)

    return info


# 存到数据库中
def save_article_content_data(info):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = '''insert into c_article_content(title, content) values (%s, %s)'''
    cursor.execute(sql, [info.title, info.content])

    conn.commit()
    cursor.close()
    conn.close()
    conn.disconnect()



def dowork():
    article_directory_link_list = get_directory_link_list_from_db()
    if article_directory_link_list:
        for item in article_directory_link_list:
            content = get_content_html(item)
            info = get_article_content(content)
            print(info.content)
            save_article_content_data(info)


if __name__ == '__main__':
    dowork()
    print('16_article_content.py done')

