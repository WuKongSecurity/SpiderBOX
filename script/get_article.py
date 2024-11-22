import json
import os
import re
import time
from urllib import parse

import yaml
import hashlib
import requests
from lxml import etree
from loguru import logger
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import urls


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
        logger.success(f"inserted success: {data['link']}")
    except DuplicateKeyError:
        logger.warning(f"article already exists: {data['link']}")


def gen_web_rid(data):
    sorted_items = sorted(data.items())
    result = "&".join(f"{key}={value}" for key, value in sorted_items)
    string = result + "ea1db124af3c7062474693fa704f4ff8"
    return hashlib.md5(string.encode(encoding='utf-8')).hexdigest()


def get_video_bilibili():
    url = "https://api.bilibili.com/x/space/wbi/arc/search"
    for mid in urls.mids:
        try:
            index = f"https://space.bilibili.com/{mid}/video"
            response_index = requests.get(index, headers=headers)
            w_webid = re.findall(r'"access_id":"(.*?)"', parse.unquote(response_index.text))[0]

            params = {
                "mid": mid,
                "ps": "30",
                "tid": "0",
                "pn": "1",
                "keyword": "",
                "order": "pubdate",
                "platform": "web",
                "web_location": "1550101",
                "order_avoided": "true",
                "dm_img_list": "[]",
                "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
                "dm_cover_img_str": "QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgR1RYIDEwNTAgKDB4MDAwMDFDODEpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKE5WSURJQS",
                "dm_img_inter": json.dumps({"ds":[{"t":2,"c":"Y2xlYXJmaXggZy1zZWFyY2ggc2VhcmNoLWNvbnRhaW5lcg","p":[1582,100,829],"s":[3,465,422]},{"t":2,"c":"d3JhcHBlcg","p":[883,73,1401],"s":[165,4144,3382]}],"wh":[4607,2504,63],"of":[322,644,322]}),
                "w_webid": w_webid,
                "wts": str(int(time.time())),
            }
            web_rid = gen_web_rid(params)
            print(web_rid)
            params["web_rid"] = web_rid

            headers_bili = headers
            headers_bili["referer"] = index
            headers_bili["origin"] = "https://space.bilibili.com"
            response = requests.get(url, headers=headers_bili, params=params)
            print(response.status_code)
            print(response.text)
        except Exception as e:
            logger.error(f"get bilibili video error: {e}")
            continue


def get_article_52pojie():
    url_list = [urls.pojie_url1, urls.pojie_url2]
    for url in url_list:
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


def read_existing_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print("Error reading existing YAML file:", e)
        return None



if __name__ == '__main__':
    # get_article_52pojie()
    get_video_bilibili()
