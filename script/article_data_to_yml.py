import os
import yaml
import requests
from datetime import datetime


ARTICLE_API = os.getenv('ARTICLE_API')
ARTICLE_TOKEN = os.getenv('ARTICLE_TOKEN')
ARTICLE_UA = os.getenv('ARTICLE_UA')  # 特殊 UA, API 防护例外规则
PROXY = os.getenv('PROXY')
YML_FILE = '../data/articles.yml'

proxies = {'http': PROXY,'https': PROXY}


def get_articles():
    headers_ip = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "sec-ch-ua": 'Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    }
    res_ip = requests.get("https://icanhazip.com/", headers=headers_ip, proxies=proxies, timeout=120)
    print("res_ip status code: ", res_ip.status_code)
    print("res_ip response: ", res_ip.text)

    print("\n========================\n")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ARTICLE_TOKEN}',
        'User-Agent': ARTICLE_UA,
    }
    response = requests.get(ARTICLE_API, headers=headers, proxies=proxies, timeout=120)
    print("get articles status code: ", response.status_code)
    print("get articles response: ", response.text)
    data = response.json()
    return data


def read_yaml():
    print(os.path.abspath(YML_FILE))
    if os.path.exists(YML_FILE):
        with open(YML_FILE, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    else:
        with open(YML_FILE, 'w', encoding='utf-8') as file:
            file.write('')
        return {}


def write_yaml(data):
    with open(YML_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def article_to_yml(data):
    # 更新时间在 10 分钟内，则需要更新（60s*1000ms*10m = 600000 毫秒）
    # time_now = int(time.time()*1000)
    # time_update = data['update_time']
    # time_diff = abs(time_now - time_update)
    # if time_diff > 600000:
    #     print('don't need update')
    #     return


    current_data = [{
        'taxonomy': '最新文章/视频',
        'icon': 'fas fa-list',
        'list': [
            {
                'term': '哔哩哔哩',
                'logo': 'images/logo/bilibili_32x32.png',
                'links': data['bilibili']
            },
            {
                'term': '公众号',
                'logo': 'images/logo/mpweixin_32x32.png',
                'links': data['weixin']
            },
            {
                'term': '吾爱破解',
                'logo': 'images/logo/52pojie_32x32.png',
                'links': data['52pojie']
            },
            {
                'term': '看雪论坛/先知社区/CSDN等',
                'logo': 'images/logo/kanxue_32x32.png',
                'links': data['other']
            },
        ]
    }]

    existing_data = read_yaml()
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if current_data != existing_data:
        write_yaml(current_data)
        print(f'update success / {time_now} / {os.path.abspath(YML_FILE)}')
    else:
        print(f'no need update / {time_now} / {os.path.abspath(YML_FILE)}')


def task():
    try:
        article = get_articles()
    except Exception as e:
        print('get article error:', e)
        return

    if not article['data']:
        print('article data is empty')
        return

    article_to_yml(article['data'])


if __name__ == '__main__':
    task()
