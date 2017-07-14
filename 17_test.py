#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import re
from urllib.parse import unquote, urljoin, urlparse
import re
import os
import sys
import configparser
import mysql.connector


import aiohttp
import arrow
import async_timeout
from bs4 import BeautifulSoup

from config import URL_PC, URL_PHONE, LOGGER, BAIDU_RN
from function import get_random_user_agent

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

async def fetch(client, url):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}

            async with client.get(url, headers=headers) as response:
                assert response.status == 200
                LOGGER.info('Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    text = await response.read()
                return text
        except Exception as e:
            LOGGER.exception(e)
            return None

# 获取url
# http: // www.baidu.com / link?url = w2bV3ST9FFL3f39PGG6VUhT10aqZ1GNZrhWa5BIclVak7hYZEh1wGiTsvrGYJgXJEAPNoPfS7x0X4xK9nLDzJK
# 转换成网址
async def get_real_url(client, url):
    with async_timeout.timeout(10):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers, allow_redirects=True) as response:
                assert response.status == 200
                LOGGER.info('Parse url: {}'.format(response.url))
                # text = ""
                # try:
                #     text = await response.text()
                # except:
                #     text = await response.read()
                # if text:
                #     print(text)
                #     text = re.findall(r'replace\(\"(.*?)\"\)', str(text))
                #     text = text[0] if text[0] else ""
                url = response.url if response.url else None
                return url
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_phone(html):
    with async_timeout.timeout(10):
        try:
            # Get title
            data_log = eval(html['data-log'])
            url = data_log.get('mu', None)
            if not url:
                return None
            # Get title
            title = html.find('h3').get_text()
            # Get author and update_time (option)
            novel_mess = html.findAll(class_='c-gap-right-large')
            basic_mess = [i.get_text() for i in novel_mess] if novel_mess else None
            return {'title': title, 'url': url, 'basic_mess': basic_mess}
        except Exception as e:
            LOGGER.exception(e)
            return None


# async def data_extraction_for_web(html):
#     with async_timeout.timeout(10):
#         try:
#             url = html.find('a').get('href', None)
#             if not url or 'baidu' in url or urlparse(url).netloc in BLACK_DOMAIN:
#                 return None
#             netloc = urlparse(url).netloc
#             is_parse = 1 if netloc in RULES.keys() else 0
#             title = html.select('font[size="3"]')[0].get_text()
#             source = html.select('font[color="#008000"]')[0].get_text()
#             time = re.findall(r'\d+-\d+-\d+', source)
#             time = time[0] if time else None
#             timestamp = 0
#             if time:
#                 try:
#                     time_list = [int(i) for i in time.split('-')]
#                     timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
#                 except Exception as e:
#                     LOGGER.exception(e)
#                     timestamp = 0
#             return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
#                     'is_parse': is_parse,
#                     'timestamp': timestamp,
#                     'netloc': netloc}
#         except Exception as e:
#             LOGGER.exception(e)
#             return None
#
#
# async def data_extraction_for_web_baidu(client, html):
#     with async_timeout.timeout(20):
#         try:
#             # 获取一段h5
#             url = html.select('h3.t a')[0].get('href', None)
#             # 获取href标签内容  -
#             # 首先 - html.select('h3.t a')[0]
#             # < a
#             # data - click = "{
#             # 'F': '778317EA',
#             # 'F1': '9D73F1E4',
#             # 'F2': '4DA6DD6B',
#             # 'F3': '54E5363F',
#             # 'T': '1497109660',
#             # 'y': 'A7BFAFBF'
#             #
#             # }" href="
#             # http: // www.baidu.com / link?url = w2bV3ST9FFL3f39PGG6VUhT10aqZ1GNZrhWa5BIclVak7hYZEh1wGiTsvrGYJgXJEAPNoPfS7x0X4xK9nLDzJK
#             # " target="
#             # _blank
#             # "><em>择天记</em>,<em>择天记</em>最新章节,<em>择天记</em>无弹窗,88读书网</a>
#
#             # 然后 - get('href', None)
#             # http: // www.baidu.com / link?url = w2bV3ST9FFL3f39PGG6VUhT10aqZ1GNZrhWa5BIclVak7hYZEh1wGiTsvrGYJgXJEAPNoPfS7x0X4xK9nLDzJK
#
#             real_url = await get_real_url(client=client, url=url) if url else None
#             if real_url:
#                 netloc = urlparse(str(real_url)).netloc
#                 # >> > import urlparse
#                 # >> > url = urlparse.urlparse('http://www.baidu.com/index.php?username=guol')
#                 # >> > print
#                 # url
#                 # ParseResult(scheme='http', netloc='www.baidu.com', path='/index.php', params='', query='username=guol',
#                 #             fragment='')
#                 # >> > print
#                 # url.netloc
#                 # www.baidu.com
#                 if 'baidu' in str(real_url) or netloc in BLACK_DOMAIN:
#                     return None
#                 #print('--------------------')
#                 #print(RULES.keys())
#                 is_parse = 1 if netloc in RULES.keys() else 0
#                 title = html.select('h3.t a')[0].get_text()
#                 # time = re.findall(r'\d+-\d+-\d+', source)
#                 # time = time[0] if time else None
#                 timestamp = 0
#                 time = ""
#                 # if time:
#                 #     try:
#                 #         time_list = [int(i) for i in time.split('-')]
#                 #         timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
#                 #     except Exception as e:
#                 #         LOGGER.exception(e)
#                 #         timestamp = 0
#                 return {'title': title, 'url': str(real_url).replace('index.html', ''), 'time': time, 'is_parse': is_parse,
#                         'timestamp': timestamp,
#                         'netloc': netloc}
#             else:
#                 return None
#         except Exception as e:
#             LOGGER.exception(e)
#             return None


# async def baidu_search(name, is_web=1):
#     url = URL_PC if is_web else URL_PHONE
#     async with aiohttp.ClientSession() as client:
#         html = await fetch(client=client, url=url, name=name, is_web=is_web)
#         if html:
#             soup = BeautifulSoup(html, 'html5lib')
#             if is_web:
#                 # result = soup.find_all(class_='f')
#                 result = soup.find_all(class_='result')
#                 #print("result = ", result)
#                 extra_tasks = [data_extraction_for_web_baidu(client=client, html=i) for i in result]
#                 tasks = [asyncio.ensure_future(i) for i in extra_tasks]
#             else:
#                 result = soup.find_all(class_='result c-result c-clk-recommend')
#                 extra_tasks = [data_extraction_for_phone(i) for i in result]
#                 tasks = [asyncio.ensure_future(i) for i in extra_tasks]
#             return await asyncio.gather(*tasks)
#









# 从数据库中获取没有被抓取过的小说链接
async def get_article_line_from_db():
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
async def get_html(url):
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all( id='list')
            print(result)
            #tasks = [asyncio.ensure_future(i) for i in get_article_directory(result)]
            #return await asyncio.gather(*tasks)


# 获取章节目录
async def get_article_directory(result):
    update_status_reg = r'<meta content="(.*?)" property="og:novel:status"/>'
    article_directory_nav_reg = r'<div class="box_con">(.*?)<div id="sidebar">'
    article_directory_reg = r'<div id="list">(.*?)<div id="footer" name="footer">'

    update_status_result = re.search(update_status_reg, result)
    article_directory_nav_result = re.findall(article_directory_nav_reg, result, re.DOTALL)[0]
    article_directory_result = re.findall(article_directory_reg, result, re.DOTALL)[0]

    title_reg = r'<h1>(.*?)</h1>'
    last_update_date_reg = r'<p>最后更新：(.*?)</p>'
    last_update_directory_reg = r'<p>最新章节：(.*?)>(.*?)</a></p>'

    article_directory_list_href_reg = r'<dd>(.*?)</dd>'
    article_directory_list_reg = r'<a href="(.*?)">(.*?)</a>'

    article_id_reg = r'<meta content="http://www.biquge.com.tw/(.*?)/" property="og:url"/'

    title_result = re.search(title_reg, article_directory_nav_result)
    last_update_date_result = re.search(last_update_date_reg, article_directory_nav_result)
    last_update_directory_result = re.search(last_update_directory_reg, article_directory_nav_result)

    article_directory_list_href_result = re.findall(article_directory_list_href_reg, article_directory_result,
                                                    re.DOTALL)
    article_id_result = re.search(article_id_reg, result)

    # 小说列表list
    article_directory_list = []
    # 小说浏览章节h5 list
    article_directory_link_list = []

    for index in article_directory_list_href_result:
        article_directory_list_result = re.search(article_directory_list_reg, index)
        info = Article_directory()
        info.article_directory_link = article_directory_list_result.group(1)
        info.article_directory = article_directory_list_result.group(2)
        # 存在这个信息就不储存
        ishave = await check_chapter_id_from_db(info)
        if ishave == False:
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
        info.article_directory = article_directory_list[i]
        info.article_directory_link = article_directory_link_list[i]
        #info.status = 1
        infos.append(info)
        #update_article_status()

    return infos



# 查看是否存在这个章节的id
async def check_chapter_id_from_db(info):

    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'select article_directory_link = %s from c_article_detail where article_directory = %s'
    cursor.execute(sql, [info.article_directory_link, info.article_directory])
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return True if len(values) > 0 else False


# 储存更新信息
async def save_article_detail(infos):

    for info in infos:
        # 存在这个信息就不储存
        ishave = await check_chapter_id_from_db(info)
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
async def update_article_status():
    conn = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    cursor = conn.cursor()
    sql = 'update c_article_detail set status = 1'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

async def dowork():

    article_list = await get_article_line_from_db()

    async with aiohttp.ClientSession() as client:
        if article_list:
            await [fetch(client,link) for link in article_list]
            for link in article_list:
                html = await fetch(client, link)
                if html:
                    soup = BeautifulSoup(html, 'html5lib')
                    result = soup.find_all('html')
                    infos = await get_article_directory(str(result))
                    await save_article_detail(infos)
                    lens = len(infos)
                    print('共需要抓取章数', lens)
                    for i in range(lens):
                        await update_article_status()
                        print('已经抓取章节进度：', i + 1)



if __name__ == '__main__':
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(dowork())
    loop.close()
    print('15_article_directory_list done')