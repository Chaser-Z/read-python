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
import threading

base_url = 'http://www.biquge.com.tw'
global main_index

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


class Article_content(object):
    __slots__ = ('content', 'status')

    def __init__(self):
        self.content = None
        self.status = None



# 获取内容那段h5
def get_content_html(urls):


    content = ""

    global main_index
    main_index = 0

    def get(url):
        try:
            r = BeautifulSoup(
                requests.get(url, timeout=120.0, headers=headers, verify=False, allow_redirects=True).content,
                'html.parser')
        except:
            pass
        else:
            if r:
                content_reg = r'<div class="content_read">(.*?)<div class="footer">'
                content = str(re.findall(content_reg, str(r), re.DOTALL))
                if content:
                    info = get_article_content(content)
                    url = url[24:]
                    print(url)
                    global main_index
                    main_index = main_index + 1
                    print('已经下载第', main_index)
                    print(info.content)
                    save_article_content_data(info, url)
                    #return content

    t1 = time.time()
    number = 0
    th = []
    # 最大的并发数量
    maxthreads = 10

    for url in urls:
        url = base_url + url
        number += 1
        t1 = threading.Thread(target=get, args=(url,))
        t1.start()
        th.append(t1)
        if number > maxthreads:
            [i.join() for i in th]
            number = 0
            th = []
    [i.join() for i in th]

    #print(time.time() - t1)


    #return content

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

def get_directory_link_from_db(id):
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()

    sql = 'select article_directory_link from c_article_detail where content is NULL and article_id = %s'
    cursor.execute(sql, [id])
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


    try:
        content = content_result.group(1)
        content = content.replace(r'\xa0\xa0\xa0\xa0', '  ')
        content = content.replace(r'<br/>\n<br/>\r\n', '\n')
        info = Article_content()
        info.content = process_html(content)
        return info

    except:
        print('----except:------')
        return None






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
    # 10_10155 16_16960
    #article_directory_link_list = get_directory_link_from_db('16_16858')
    article_directory_link_list = get_directory_link_list_from_db()
    total_num = len(article_directory_link_list)
    print('需要下载章节数:', total_num)
    content = get_content_html(article_directory_link_list)
    #info = get_article_content(content)
    # if info:
    #     pass
    #     #print('已经下载第', index)
    #     # interval = random.uniform(1, 3)
    #     # time.sleep(interval)
    #     #save_article_content_data(info, item)
    # #if article_directory_link_list:
    #     #for index,item in enumerate(article_directory_link_list):



if __name__ == '__main__':
    dowork()
    print('16_article_content.py done')

