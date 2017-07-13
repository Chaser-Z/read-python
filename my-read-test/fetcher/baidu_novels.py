#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import re
from urllib.parse import urlparse

import aiohttp
import arrow
import async_timeout
from bs4 import BeautifulSoup

from config.config import URL_PC, URL_PHONE, LOGGER, BAIDU_RN
from config.rules import BLACK_DOMAIN, RULES
from fetcher.function import get_random_user_agent


async def fetch(client, url, name, is_web):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}
            if is_web:
                params = {'wd': name, 'ie': 'utf-8', 'rn': BAIDU_RN, 'vf_bl': 1}
            else:
                params = {'word': name}
            async with client.get(url, params=params, headers=headers) as response:
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


async def data_extraction_for_web(html):
    with async_timeout.timeout(10):
        try:
            url = html.find('a').get('href', None)
            if not url or 'baidu' in url or urlparse(url).netloc in BLACK_DOMAIN:
                return None
            netloc = urlparse(url).netloc
            is_parse = 1 if netloc in RULES.keys() else 0
            title = html.select('font[size="3"]')[0].get_text()
            source = html.select('font[color="#008000"]')[0].get_text()
            time = re.findall(r'\d+-\d+-\d+', source)
            time = time[0] if time else None
            timestamp = 0
            if time:
                try:
                    time_list = [int(i) for i in time.split('-')]
                    timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
                except Exception as e:
                    LOGGER.exception(e)
                    timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_web_baidu(client, html):
    with async_timeout.timeout(20):
        try:
            # 获取一段h5
            url = html.select('h3.t a')[0].get('href', None)
            # 获取href标签内容  -
            # 首先 - html.select('h3.t a')[0]
            # < a
            # data - click = "{
            # 'F': '778317EA',
            # 'F1': '9D73F1E4',
            # 'F2': '4DA6DD6B',
            # 'F3': '54E5363F',
            # 'T': '1497109660',
            # 'y': 'A7BFAFBF'
            #
            # }" href="
            # http: // www.baidu.com / link?url = w2bV3ST9FFL3f39PGG6VUhT10aqZ1GNZrhWa5BIclVak7hYZEh1wGiTsvrGYJgXJEAPNoPfS7x0X4xK9nLDzJK
            # " target="
            # _blank
            # "><em>择天记</em>,<em>择天记</em>最新章节,<em>择天记</em>无弹窗,88读书网</a>

            # 然后 - get('href', None)
            # http: // www.baidu.com / link?url = w2bV3ST9FFL3f39PGG6VUhT10aqZ1GNZrhWa5BIclVak7hYZEh1wGiTsvrGYJgXJEAPNoPfS7x0X4xK9nLDzJK

            real_url = await get_real_url(client=client, url=url) if url else None
            if real_url:
                netloc = urlparse(str(real_url)).netloc
                # >> > import urlparse
                # >> > url = urlparse.urlparse('http://www.baidu.com/index.php?username=guol')
                # >> > print
                # url
                # ParseResult(scheme='http', netloc='www.baidu.com', path='/index.php', params='', query='username=guol',
                #             fragment='')
                # >> > print
                # url.netloc
                # www.baidu.com
                if 'baidu' in str(real_url) or netloc in BLACK_DOMAIN:
                    return None
                #print('--------------------')
                #print(RULES.keys())
                is_parse = 1 if netloc in RULES.keys() else 0
                title = html.select('h3.t a')[0].get_text()
                # time = re.findall(r'\d+-\d+-\d+', source)
                # time = time[0] if time else None
                timestamp = 0
                time = ""
                # if time:
                #     try:
                #         time_list = [int(i) for i in time.split('-')]
                #         timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
                #     except Exception as e:
                #         LOGGER.exception(e)
                #         timestamp = 0
                return {'title': title, 'url': str(real_url).replace('index.html', ''), 'time': time, 'is_parse': is_parse,
                        'timestamp': timestamp,
                        'netloc': netloc}
            else:
                return None
        except Exception as e:
            LOGGER.exception(e)
            return None


async def baidu_search(name, is_web=1):
    url = URL_PC if is_web else URL_PHONE
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, name=name, is_web=is_web)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            if is_web:
                # result = soup.find_all(class_='f')
                result = soup.find_all(class_='result')
                #print("result = ", result)
                extra_tasks = [data_extraction_for_web_baidu(client=client, html=i) for i in result]
                tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            else:
                result = soup.find_all(class_='result c-result c-clk-recommend')
                extra_tasks = [data_extraction_for_phone(i) for i in result]
                tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            return await asyncio.gather(*tasks)


