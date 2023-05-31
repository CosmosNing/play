import requests
import json
import time
import random
import xml.dom.minidom
from datetime import datetime


def gen_rss(notice_list):
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S +0800'

    doc = xml.dom.minidom.Document()
    rss = doc.createElement('rss')
    rss.setAttribute('version', '2.0')
    doc.appendChild(rss)

    channel = doc.createElement('channel')
    rss.appendChild(channel)

    title = doc.createElement('title')
    title.appendChild(doc.createTextNode('南京市人才安居信息服务平台'))
    channel.appendChild(title)
    link = doc.createElement('link')
    link.setAttribute('rel', 'alternate')
    link.setAttribute('type', 'text/html')
    link.setAttribute('href', 'http://rcaj.nanjing.gov.cn/zhzbweb/m.html')
    channel.appendChild(link)

    for notice in notice_list:
        item = doc.createElement('item')

        item_title = doc.createElement('title')
        item_title.appendChild(doc.createTextNode(notice['name']))
        item.appendChild(item_title)

        item_link = doc.createElement('link')
        item_link.appendChild(doc.createTextNode(
            'http://rcaj.nanjing.gov.cn/zhzbweb/views/modules/rcaj/template.html?url=/zhzbweb/rcaj/tRcajTzgg&id=' +
            notice['id']))
        item.appendChild(item_link)

        notice['content'] = notice['content'].replace('&lt;', '<')
        notice['content'] = notice['content'].replace('&gt;', '>')
        notice['content'] = notice['content'].replace('&quot;', '"')
        notice['content'] = notice['content'].replace('&amp;', '&')
        desc = doc.createElement('description')
        desc.appendChild(doc.createCDATASection(notice['content']))
        item.appendChild(desc)

        pubDate = doc.createElement('pubDate')
        pubDate.appendChild(doc.createTextNode(
            datetime.fromtimestamp(datetime.strptime(notice['createDate1'], '%Y-%m-%d').timestamp()).strftime(
                GMT_FORMAT)))
        item.appendChild(pubDate)

        channel.appendChild(item)

    with open("998_run_all.xml", 'w', encoding="utf-8") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


def get_notice_list():
    url = "http://rcaj.nanjing.gov.cn/zhzbweb/rcaj/tRcajTzgg?name&pageNo=1&pageSize"
    payload = {}
    headers = {
        'Cookie': 'pageNo=1; pageSize=5'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_text = json.loads(response.text)
    total_page = json_text['totalPage']

    notice_list = json_text['list']
    for i in range(2, total_page + 1):
        url = "http://rcaj.nanjing.gov.cn/zhzbweb/rcaj/tRcajTzgg?name&pageNo=" + str(i) + "&pageSize"
        print(url)
        time.sleep(5 + random.randint(1, 10))
        response = requests.request("POST", url, headers=headers, data=payload)
        json_text = json.loads(response.text)
        notice_list.extend(json_text['list'])
    return notice_list


if __name__ == "__main__":
    gen_rss(get_notice_list())
