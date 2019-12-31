import os
import re

import pandas as pd
import requests
import time
import xlsxwriter
from lxml import html
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

headers_zgzqb = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

headers_shzqb = {
    'Cookie': 'PHPSESSID=2atnfohs45ffj9srpjh1ks82r3; cnstock_username=huangjt; cnstock_ss=8d4936c45cc14c5285e4de4c9782ff39; cnstock_record=1577248339761; CNSTOCK_SSO="ex=&BBS=huangjt|8nre%2FqPhNRE7ZWyLCstRog%3D%3D&SCHOOL=huangjt|0YHH23%2BFekW1KyR%2FXZoTyA%3D%3D&BLOG=huangjt|ADxtS1naKfss2d8j9eSkTQ%3D%3D&SHOP=huangjt|FuAGmrQxEamWm%2FszmUyy7w%3D%3D&ec="; CNSTOCK_BLOG=SUQ9MzM4NDk5Jk5BTUU9aHVhbmdqdCZFTUFJTD1XV3h6WWpVek5EUXpPRFl6TXpnelh6YzFQV1p4ZG5keVptNWhabkp3; CNSTOCK_PASSPORT="ex=&ID=338499&NAME=huangjt&EMAIL=WWxzYjUzNDQzODYzMzgzXzc1PWZxdndyZm5hZnJw&ec="; CNSTOCK_REALSSO=eWswWm9obDV6WC80YkhiSTlZYjNvZmptTlVwdlBqVEdqMlRjSXNuUEdtT096KzRQOGlMdzlqK3FIdDRmS004eCwzMzg0OTksaHVhbmdqdCxXV3h6WWpVek5EUXpPRFl6TXpnelh6YzFQV1p4ZG5keVptNWhabkp3LDE1NzcyNDgyNTMzNjI%3D;  ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

paper_path = r'E:\securities_paper'

search_key = '创金合信'


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.process_time()
        fn(*args, **kwargs)
        print("%s cost %s second" % (fn.__name__, time.process_time() - start))

    return _wrapper


def get_date(start, end):
    return pd.date_range(start=start, end=end)


# 证券日报电子报
def zqrb(date):
    path = os.path.join(paper_path, '证券日报电子报', date + '.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='UTF-8') as f:
            return parse_zqrb(date, f.read())
    else:
        url = 'http://epaper.zqrb.cn/html/{}/{}/node_2.htm'.format(date[0:7], date[8:])
        r = requests.get(url, headers=headers)
        save_html('证券日报电子报', date, r.content, 'UTF-8')
        if r.status_code == 200:
            return parse_zqrb(date, r.content.decode("utf-8"))
        elif r.status_code == 404:
            print('未找到页面')
            return []
        else:
            print('页面异常')
            return []


# 证券日报电子报
def parse_zqrb(date, content):
    data_list = []
    _html = html.fromstring(content)
    # print(html)
    title = _html.xpath('//title')[0].text
    # print(title)
    if title == '404 Not Found':
        # print('页面不存在')
        return []
    paper_list = _html.xpath('//a[@class="vote_content12px"]')
    # print(paper_list)
    if len(paper_list) == 0:
        print('页面解析异常')
        return []
    for paper in paper_list:
        # print(paper.text)
        title = paper.text_content().strip()
        if search_key in title:
            # 去除
            title = re.sub('[（|(]下转.*版[）|)]', '', title)
            title = re.sub('[（|(]上接.*版[）|)]', '', title)
            data = {'title': title, 'date': date, 'source': '证券日报电子报'}
            # print(data)
            data_list.append(data)

    # print(data_list)
    return data_list


# 证券时报电子报
def zqsb(date):
    path = os.path.join(paper_path, '证券时报电子报', date + '.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='UTF-8') as f:
            return parse_zqsb(date, f.read())
    else:
        url = 'http://epaper.stcn.com/paper/zqsb/html/{}/{}/node_2.htm'.format(date[0:7], date[8:])
        r = requests.get(url, headers=headers)
        save_html('证券时报电子报', date, r.content, 'UTF-8')
        if r.status_code == 200:
            return parse_zqsb(date, r.content.decode("utf-8"))
        elif r.status_code == 404:
            print('未找到页面')
            return []
        else:
            print('页面异常')
            return []


# 证券时报电子报
def parse_zqsb(date, content):
    data_list = []
    if len(content) <= 1:
        # print('页面为空')
        return []
    if content.replace("\n", "") == '<script>window.location="/paper/zqsb/html/epaper/index/index.htm";</script>':
        # print('页面不存在')
        return []

    # print(r.content.decode("utf-8"))
    _html = html.fromstring(content)

    # title = _html.xpath('//title')[0].text
    # print(title)
    # print(html)
    # 2015/11/30
    # if date < '2015-11-30':
    paper_list = _html.xpath('//div[@id="listWrap"]/div/ul/li/a')
    if len(paper_list) == 0:
        paper_list = _html.xpath('//div[@id="webtree"]/dl/dd/ul/li/a')
    # print(paper_list)
    if len(paper_list) == 0:
        print('页面解析异常')
        return []
    for paper in paper_list:
        # print(paper.text)
        title = paper.text_content().strip()
        if search_key in title:
            data = {'title': title, 'date': date, 'source': '证券时报电子报'}
            # print(data)
            data_list.append(data)

    # print(data_list)
    return data_list


# 中国证券报
def zgzqb(date):
    path = os.path.join(paper_path, '中国证券报', date + '.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='UTF-8') as f:
            return parse_zgzqb(date, f.read())
    else:
        if date < '2018-02-06' or date > '2018-03-28':
            url = 'http://epaper.cs.com.cn/zgzqb/html/{}/{}/nbs.D110000zgzqb_A01.htm'.format(date[0:7], date[8:])
        else:
            url = 'http://epaper.cs.com.cn/zgzqb/html/{}/{}/nbs.D110000zgzqb_A02.htm'.format(date[0:7], date[8:])
        r = requests.get(url, headers=headers_zgzqb)
        save_html('中国证券报', date, r.content, 'UTF-8')
        if r.status_code == 200:
            return parse_zgzqb(date, r.content.decode("utf-8"))
        elif r.status_code == 404:
            print('未找到页面')
            return []
        else:
            print('页面异常')
            return []


# 中国证券报
def parse_zgzqb(date, content):
    data_list = []
    _html = html.fromstring(content)
    title = _html.xpath('//title')[0].text
    # print(title)
    if title == '提示':
        # print('页面不存在')
        return []

    paper_list = _html.xpath('//tr[@class="default1"]//a')
    # print(paper_list)
    if len(paper_list) == 0:
        print('页面解析异常')
        return []
    for paper in paper_list:
        # print(paper.text)
        title = paper.text_content().strip()
        if search_key in title:
            data = {'title': title, 'date': date, 'source': '中国证券报'}
            # print(data)
            data_list.append(data)
    # print(data_list)
    return data_list


# 上海证券报
def shzqb(date):
    path = os.path.join(paper_path, '上海证券报', date + '.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return parse_shzqb(date, f.read())
    else:
        url = 'http://paper.cnstock.com/html/{}/{}/node_3.htm'.format(date[0:7], date[8:])
        r = requests.get(url, headers=headers_shzqb)
        save_html('上海证券报', date, r.content.decode(r.apparent_encoding).encode("utf-8"), 'GB2312')
        if r.status_code == 200:
            return parse_shzqb(date, r.content.decode(r.apparent_encoding))
        elif r.status_code == 404:
            print('未找到页面')
            return []
        else:
            print('页面异常')
            return []


# 上海证券报
def parse_shzqb(date, content):
    data_list = []
    _html = html.fromstring(content)
    title = _html.xpath('//title')[0].text
    # print(title)
    if title == '对不起，页面不存在了，请选择其它页面访问。':
        # print('页面不存在')
        return []
    paper_list = _html.xpath('//div[@id="nlist"]//ul/li/a')
    # print(paper_list)
    if len(paper_list) == 0:
        print('页面解析异常')
        return []
    for paper in paper_list:
        # print(paper.text_content())
        title = paper.text_content().strip()
        if search_key in title:
            data = {'title': title, 'date': date, 'source': '上海证券报'}
            # print(data)
            data_list.append(data)
    # print(data_list)
    return data_list


def create_excel(datas, name):
    # 新建一个Excel文件
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(name))
    # 新建一个工作表
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format({'bold': True})

    tabletitle = ['公告', '披露日期', '数据源']

    for i in range(0, len(tabletitle)):
        worksheet.write(0, i, tabletitle[i], title_format)

    for i in range(0, len(datas)):
        worksheet.write(i + 1, 0, datas[i]['title'])
        worksheet.write(i + 1, 1, datas[i]['date'])
        worksheet.write(i + 1, 2, datas[i]['source'])

    workbook.close()


def save_html(file_type, file_name, file_content, encoding):
    root_path = os.path.join(paper_path, file_type)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    file_path = os.path.join(root_path, file_name + '.html')
    with open(file_path, 'wb') as f:
        f.write(file_content)


def save_file(file_name, data):
    """
    把文件存成csv格式的文件，header 写出列名，index写入行名称
    :param list: 要存储的一条列表数据
    :return:
    """
    df = pd.DataFrame(data=[data])
    df.to_csv(file_name + '.csv', encoding="utf-8-sig", mode="a", header=False, index=False)


def save_csv(file_name, list):
    """
    一次性存储完
    :return:
    """
    pf = pd.DataFrame(data=list)
    pf.to_csv(file_name + '.csv', encoding="utf-8-sig", header=False, index=False)


def crawl_paper(start, end):
    zqrb_list = []
    zqsb_list = []
    zgzqb_list = []
    shzqb_list = []
    dates = list(get_date(start, end))
    # dates = list(get_date('2017-11-12', '2017-11-12'))
    for date in dates:
        print(date)
        zqrb_list.extend(zqrb(str(date)[0:10]))
        # zqsb_list.extend(zqsb(str(date)[0:10]))
        # zgzqb_list.extend(zgzqb(str(date)[0:10]))
        # shzqb_list.extend(shzqb(str(date)[0:10]))

        # create_excel(zqrb_list, '证券日报电子报')
        # create_excel(zqsb_list, '证券时报电子报')
        # create_excel(zgzqb_list, '中国证券报')
        # create_excel(shzqb_list, '上海证券报')


if __name__ == '__main__':
    # parse_zqrb(None)
    paper_list = []
    zqrb_list = []
    zqsb_list = []
    zgzqb_list = []
    shzqb_list = []
    dates = list(get_date('2014-7-1', '2019-12-26'))
    # dates = list(get_date('2017-11-12', '2017-11-12'))
    pbar = tqdm(dates)
    for date in pbar:
        # print(date)
        _list1 = zqrb(str(date)[0:10])
        zqrb_list.extend(_list1)
        _list2 = zqsb(str(date)[0:10])
        zqsb_list.extend(_list2)
        _list3 = zgzqb(str(date)[0:10])
        zgzqb_list.extend(_list3)
        _list4 = shzqb(str(date)[0:10])
        shzqb_list.extend(_list4)

        _list = _list1 + _list2 + _list3 + _list4
        if len(_list) > 0:
            # paper_list.append({'date': date, 'data': _list})
            paper_list.extend(_list)

        pbar.set_description("进度 %s" % str(date)[0:10])

    # save_csv('paper\证券日报电子报', zqrb_list)
    # save_csv('paper\证券时报电子报', zqsb_list)
    # save_csv('paper\中国证券报', zgzqb_list)
    # save_csv('paper\上海证券报', shzqb_list)

    # create_excel(zqrb_list, '证券日报电子报')
    # create_excel(zqsb_list, '证券时报电子报')
    # create_excel(zgzqb_list, '中国证券报')
    # create_excel(shzqb_list, '上海证券报')

    # pbar = tqdm(paper_list)
    # for paper in pbar:
    #     save_file('haha', paper)
    # pbar.set_description("进度 %s" % paper)

    df = pd.DataFrame(data=paper_list)
    print(df.count())
    # 去重
    df = df.drop_duplicates()
    print(df.count())
    for ir in df.itertuples():
        print(ir[1], ir[2], ir[3])
    g = df.groupby(['date', 'title']).apply(lambda x: ','.join(x['source'])).reset_index()
    print('----------------------------------')

    # sum_result = g.sum().reset_index()
    #
    for ir in g.itertuples():
        print(ir[1], ir[2], ir[3])

    g.to_csv('喵喵喵' + '.csv', encoding="utf-8-sig", header=False, index=False)
