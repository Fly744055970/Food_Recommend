import os.path

import requests
from lxml import html
import time
import re

import csv
etree = html.etree

if not os.path.exists('food1.csv'):
    fp = open('food1.csv', 'a+', encoding='utf-8-sig',newline='')
    csv_writer = csv.writer(fp)
    csv_writer.writerow(["图片", '标题', "简介", "作者", "收藏数量", "评论数量","类型"])
else:
    fp = open('food1.csv', 'a+', encoding='utf-8-sig',newline='')
    csv_writer = csv.writer(fp)

for i in range(17):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    # url ='https://www.ecook.cn/shicai/12362/?page={}'.format(i)#鲁菜
    # url ='https://www.ecook.cn/caipu/fenlei257352920/?page={}'.format(i)#川菜
    # url = 'https://www.ecook.cn/shicai/5325/?page={}'.format(i)  # 西餐
    # url = 'https://www.ecook.cn/caipu/fenlei257353790/?page={}'.format(i)  # 运孕婴
    # url = 'https://www.ecook.cn/shicai/17849/?page={}'.format(i)  # 减肥
    # url ='https://www.ecook.cn/shicai/5354/?page={}?'.format(i)#湘菜
    # url ='https://www.ecook.cn/caipu/fenlei257352988/?page={}'.format(i)#粤菜
    url ='https://www.ecook.cn/shicai/4032/?page={}'.format(i+1)#云南

    page_text = requests.get(url=url,headers=headers).text
    html.encoding = 'utf-8'
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//ul[@class="menu_list"][1]/li')

    for li in li_list:
        try:
            imgurl = li.xpath('.//a/div/img/@src')[0]
            title = li.xpath('.//div[@class="txt"]/a/h4/text()')[0]
            jianjie = li.xpath('.//div[@class="txt"]/a/p/text()')[0]
            author = li.xpath('.//div[@class="writer"]/a/text()')[0]
            shoucang = li.xpath('.//div[@class="list_collect"]/span/text()')[0]
            pinglun = li.xpath('.//div[@class="praise"]/span/text()')[0]
            csv_writer.writerow([imgurl, title,jianjie,author,shoucang,pinglun,'川菜'])
            print([imgurl, title,jianjie,author,shoucang,pinglun])
        except:
            print('本条爬取失败')
        # filename.close()
fp.close()
print("over")


