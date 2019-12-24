import requests
from lxml import etree
from lxml import html
import pandas as pd
import xlsxwriter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

headers_zgzqb = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

search_key = '创金'


def get_date(start, end):
    return pd.date_range(start=start, end=end)


# 证券日报电子报
def parse_zqrb(date):
    data_list = []
    url = 'http://epaper.zqrb.cn/html/{}/{}/node_2.htm'.format(date[0:7], date[8:])
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = etree.HTML(r.content.decode("utf-8"))
        # print(html)
        paper_list = html.xpath('//a[@class="vote_content12px"]')
        # print(paper_list)
        if len(paper_list) == 0:
            print('页面解析异常')
        for paper in paper_list:
            # print(paper.text)
            title = paper.text
            if search_key in title:
                data = {'title': title, 'date': date, 'source': '证券日报电子报'}
                # print(data)
                data_list.append(data)
    elif r.status_code == 404:
        print('未找到页面')
    else:
        print('页面异常')
    print(data_list)
    return data_list


# 证券时报电子报
def parse_zqsb(date):
    data_list = []
    url = 'http://epaper.stcn.com/paper/zqsb/html/{}/{}/node_2.htm'.format(date[0:7], date[8:])
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        if r.text.replace("\n", "") == '<script>window.location="/paper/zqsb/html/epaper/index/index.htm";</script>':
            print('页面重定向')
            return data_list

        # print(r.content.decode("utf-8"))
        html = etree.HTML(r.content.decode("utf-8"))
        # print(html)
        # 2015/11/30
        if date < '2015/11/30':
            paper_list = html.xpath('//div[@id="listWrap"]/div/ul/li/a')
        else:
            paper_list = html.xpath('//div[@id="webtree"]/dl/dd/ul/li/a')
        # print(paper_list)
        if len(paper_list) == 0:
            print('页面解析异常')
        for paper in paper_list:
            # print(paper.text)
            title = paper.text
            if search_key in title:
                data = {'title': title, 'date': date, 'source': '证券时报电子报'}
                # print(data)
                data_list.append(data)
    elif r.status_code == 404:
        print('未找到页面')
    else:
        print('页面异常')
    print(data_list)
    return data_list


# 中国证券报
def parse_zgzqb(date):
    data_list = []
    url = 'http://epaper.cs.com.cn/zgzqb/html/{}/{}/nbs.D110000zgzqb_A01.htm'.format(date[0:7], date[8:])
    r = requests.get(url, headers=headers_zgzqb)
    if r.status_code == 200:
        _html = html.fromstring(r.content.decode("utf-8"))
        paper_list = _html.xpath('//tr[@class="default1"]//a')
        # print(paper_list)
        if len(paper_list) == 0:
            print('页面解析异常')
        for paper in paper_list:
            # print(paper.text)
            title = paper.text_content()
            if search_key in title:
                data = {'title': title, 'date': date, 'source': '中国证券报'}
                # print(data)
                data_list.append(data)
    elif r.status_code == 404:
        print('未找到页面')
    else:
        print('页面异常')
    print(data_list)
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


if __name__ == '__main__':
    # parse_zqrb(None)
    zqrb_list = []
    zqsb_list = []
    zgzqb_list = []
    dates = list(get_date('2014-7-1', '2017-4-30'))
    # dates = list(get_date('2014-9-11', '2014-9-11'))
    for date in dates:
        print(date)
        # zqrb_list.extend(parse_zqrb(str(date)[0:10]))
        # zqsb_list.extend(parse_zqsb(str(date)[0:10]))
        zgzqb_list.extend(parse_zgzqb(str(date)[0:10]))

    # create_excel(zqrb_list, '证券日报电子报')
    # create_excel(zqsb_list, '证券时报电子报')
    create_excel(zgzqb_list, '中国证券报')
