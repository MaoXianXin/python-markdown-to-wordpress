import requests
import json
from tomd import Tomd
import pandas as pd
import re


def escape_characters(article_content):
    to_origin = {'&gt;': '>', '&lt;': '<', '&#61;': '=', '&#34;': '"', '&#64;': '@', '&#xff1a;': ':', '&#43;': '+'}
    for key in to_origin.keys():
        article_content = re.sub(key, to_origin[key], article_content)
    return article_content


def get_article_md(articleIds):
    articleIds = str(articleIds)
    url = "http://pre-blog-api.csdn.net/phoenix/api/v1/batch-get-article-content?articleIds=" + articleIds

    payload = {}
    headers = {
        'Cookie': 'dc_session_id=10_1647485189147.409158; dc_sid=131f38fcc146511806d31a505a27cf8e; uuid_tt_dd=10_35467775200-1647485189147-220278'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    content = json.loads(response.content)
    article_title = content['data'][articleIds]['title']
    article_content = content['data'][articleIds]['content']
    article_content = escape_characters(article_content)
    article_content = '<p>' + '转载自: ' + 'https://blog.csdn.net/' + content['data'][articleIds][
        'username'] + '/article/details/' + articleIds + '</p>' + article_content

    markdown = Tomd(article_content).markdown
    with open('./md_files/' + str(article_title) + '.md', 'w', encoding='utf-8') as file:
        file.write(markdown)


article_list = list(set(pd.read_csv('article_id.csv')['artile_id']))
for id in article_list:
    get_article_md(id)

# get_article_md(73109328)
print('done')
