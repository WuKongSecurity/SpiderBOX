import re
import json
import time
import base64
import random
import schedule
import threading
from urllib import parse

import hashlib
import requests
from lxml import etree
from loguru import logger
from datetime import datetime
from urllib.parse import quote

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import urls


logger.add('./log/{time}.log', rotation='00:00', retention="10 days", compression='zip', encoding="utf8")
client = MongoClient('mongodb://localhost:27017/')
db = client['spiderbox']
collection = db['article']


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
}

def md5_hash(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def save_to_mongodb(data):
    md5_id = md5_hash(data['link'])
    data['_id'] = md5_id
    try:
        collection.insert_one(data)
        logger.success(f"inserted success: {data['platform']} / {data['link']} / {data['title']}")
    except DuplicateKeyError:
        logger.warning(f"article already exists: {data['platform']} / {data['link']} / {data['title']}")


def gen_w_rid(data):
    sorted_items = sorted(data.items())
    result = []
    for key, value in sorted_items:
        result.append(f"{key}={quote(str(value))}")
    result = "&".join(result)
    string = result + "ea1db124af3c7062474693fa704f4ff8"
    return hashlib.md5(string.encode(encoding='utf-8')).hexdigest()


def base64_string(string):
    utf8_bytes = string.encode('utf-8')
    base64_str = base64.b64encode(utf8_bytes).decode('utf-8')
    return base64_str[:-2]


def get_win_width_height(win_width, win_height):
    random_value = random.randint(0, 113)
    return [
        2 * win_width + 2 * win_height + 3 * random_value,
        4 * win_width - win_height + random_value,
        random_value
    ]

def get_scroll_top_left(scroll_top, scroll_left):
    random_value = random.randint(0, 513)
    return [
        3 * scroll_top + 2 * scroll_left + random_value,
        4 * scroll_top - 4 * scroll_left + 2 * random_value,
        random_value
    ]


def get_video_bilibili():
    url = "https://api.bilibili.com/x/space/wbi/arc/search"
    for mid in urls.bilibili_bloggers:
        try:
            index = f"https://space.bilibili.com/{mid}/video"
            response_index = requests.get(index, headers=headers)
            w_webid = re.findall(r'"access_id":"(.*?)"', parse.unquote(response_index.text))[0]
            dm_img_str = base64_string('WebGL 1.0 (OpenGL ES 2.0 Chromium)')
            dm_cover_img_str = base64_string('ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x00001F15) Direct3D11 vs_5_0 ps_5_0, D3D11)Google Inc. (NVIDIA)')
            dm_img_inter = {
                "ds": [],
                "wh": get_win_width_height(2560, 1440),
                "of": get_scroll_top_left(0, 0),
            }
            params = {
                "mid": mid,
                "ps": 30,
                "tid": 0,
                "pn": 1,
                "keyword": "",
                "order": "pubdate",
                "platform": "web",
                "web_location": 1550101,
                "order_avoided": "true",
                "dm_img_list": "[]",
                "dm_img_str": dm_img_str,
                "dm_cover_img_str": dm_cover_img_str,
                "dm_img_inter": json.dumps(dm_img_inter, separators=(',', ':')),
                "w_webid": w_webid,
                "wts": str(int(time.time())),
            }
            w_rid = gen_w_rid(params)
            params["w_rid"] = w_rid
            headers_bili = headers
            headers_bili["referer"] = index
            headers_bili["origin"] = "https://space.bilibili.com"
            response = requests.get(url, headers=headers_bili, params=params).json()
            video_list = response["data"]["list"]["vlist"]
            for video in video_list:
                dt = datetime.fromtimestamp(video["created"])
                release_time_format = dt.strftime("%Y-%m-%d %H:%M:%S")
                release_time_stamp = video["created"] * 1000
                data = {
                    "platform": "bilibili",
                    "title": video["title"],
                    "link": "https://www.bilibili.com/video/" + video["bvid"],
                    "author": video["author"],
                    "release_time_format": release_time_format,
                    "release_time_stamp": release_time_stamp,
                    "created_time_stamp": int(time.time() * 1000)
                }
                save_to_mongodb(data)
        except Exception as e:
            logger.error(f"get bilibili video error: {e}")
            continue
        logger.info(f"="*60)
        logger.info(f"get bilibili video success: {mid}")
        logger.info(f"=" * 60)
        time.sleep(3)


def get_article_52pojie():
    for url in urls.pojie_urls:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html = etree.HTML(response.text)
                article_list = html.xpath('//tbody[contains(@id, "normalthread_")]')
                for article in article_list:
                    title = article.xpath('.//th/a[@class="s xst"]/text()')[0].strip()
                    link = article.xpath('.//th/a[@class="s xst"]/@href')[0].strip()
                    author = article.xpath('.//td[@class="by"][1]/cite/a/text()')[0].strip()
                    release_time_format = article.xpath('.//td[@class="by"][1]/em/span/text()')[0].strip()
                    dt = datetime.strptime(release_time_format, "%Y-%m-%d %H:%M")
                    release_time_stamp = int(dt.timestamp() * 1000)
                    data = {
                        "platform": "52pojie",
                        "title": title,
                        "link": "https://www.52pojie.cn/" + link,
                        "author": author,
                        "release_time_format": release_time_format,
                        "release_time_stamp": release_time_stamp,
                        "created_time_stamp": int(time.time() * 1000)
                    }
                    save_to_mongodb(data)
        except Exception as e:
            logger.error(f"get 52pojie article error: {e}")
            continue


def get_article_csdn():
    # rss: https://rss.csdn.net/username/rss/map
    url = "https://blog.csdn.net/community/home-api/v1/get-business-list"
    for bloggers in urls.csdn_bloggers:
        username = bloggers[0]
        author = bloggers[1]
        try:
            params = {
                "page": 1,
                "size": 10,
                "businessType": "blog",
                "orderby": "",
                "noMore": False,
                "year": "",
                "month": "",
                "username": username,
                "filterType": "",
                "blogType": "ViewCount"
            }
            headers_csdn = headers
            headers_csdn["referer"] = f"https://blog.csdn.net/{username}?type=blog"
            response = requests.get(url, headers=headers_csdn, params=params).json()
            article_list = response["data"]["list"]
            for article in article_list:
                release_time_format = article["postTime"]
                dt = datetime.strptime(release_time_format, "%Y-%m-%d %H:%M:%S")
                release_time_stamp = int(dt.timestamp() * 1000)
                data = {
                    "platform": "csdn",
                    "title": article["title"],
                    "link": article["url"],
                    "author": author,
                    "release_time_format": release_time_format,
                    "release_time_stamp": release_time_stamp,
                    "created_time_stamp": int(time.time() * 1000)
                }
                save_to_mongodb(data)
        except Exception as e:
            logger.error(f"get csdn article error: {e}")
            continue
        logger.info(f"="*60)
        logger.info(f"get csdn article success: {username} / {author}")
        logger.info(f"=" * 60)
        time.sleep(2)


def get_article_xz():
    headers_xz = headers
    headers_xz["referer"] = "https://xz.aliyun.com/node/23"
    try:
        response = requests.get(urls.xz_url, headers=headers_xz)
        html = etree.HTML(response.text)
        article_list = html.xpath("//table//tr")
        for article in article_list:
            title = article.xpath('.//a[@class="topic-title"]/text()')[0].strip()
            link = article.xpath('.//a[@class="topic-title"]/@href')[0].strip()
            author = article.xpath('.//p[@class="topic-info"]/a[1]/text()')[0].strip()
            release_time_format = "".join(article.xpath('.//p[@class="topic-info"]/text()'))
            release_time_format = re.findall(r"\d{4}-\d{2}-\d{2}", release_time_format)[0]
            dt = datetime.strptime(release_time_format, "%Y-%m-%d")
            release_time_stamp = int(dt.timestamp() * 1000)
            data = {
                "platform": "xz",
                "title": title,
                "link": "https://xz.aliyun.com" + link,
                "author": author,
                "release_time_format": release_time_format,
                "release_time_stamp": release_time_stamp,
                "created_time_stamp": int(time.time() * 1000)
            }
            save_to_mongodb(data)
    except Exception as e:
        logger.error(f"get xz article error: {e}")


def get_article_kanxue():
    headers_kanxue = headers
    headers_kanxue["referer"] = "https://bbs.kanxue.com/forum-151.htm"
    for url in urls.kanxue_urls:
        try:
            response = requests.get(url, headers=headers_kanxue)
            html = etree.HTML(response.text)
            article_list = html.xpath('//tbody/tr[@class="thread "]')
            for article in article_list:
                title = article.xpath('.//div[1]/a[2]/text()')[0].strip()
                link = article.xpath('.//div[1]/a[2]/@href')[0].strip()
                author = article.xpath('.//div[2]//a/text()')[0].strip()
                release_time_format = article.xpath('.//div[2]/div[1]/span[1]/text()')[0].strip()
                release_time_format = release_time_format.replace("・", "").strip()
                if "[求助]" not in title and "[注意]" not in title and "[调查]" not in title and "[建议]" not in title:
                    data = {
                        "platform": "xz",
                        "title": title,
                        "link": "https://bbs.kanxue.com/" + link,
                        "author": author,
                        "release_time_format": release_time_format,
                        "release_time_stamp": "",
                        "created_time_stamp": int(time.time() * 1000)
                    }
                    save_to_mongodb(data)
        except Exception as e:
            logger.error(f"get kanxue article error: {e}")


def task():
    thread1 = threading.Thread(target=get_article_52pojie)
    thread2 = threading.Thread(target=get_video_bilibili)
    thread3 = threading.Thread(target=get_article_csdn)
    thread4 = threading.Thread(target=get_article_xz)
    thread5 = threading.Thread(target=get_article_kanxue)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    logger.success("get all article success!")


if __name__ == '__main__':
    # 每隔 15 分钟运行一次
    schedule.every(15).minutes.do(task)
    while True:
        schedule.run_pending()
