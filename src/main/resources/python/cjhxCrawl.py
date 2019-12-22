import json

import os
import requests
import time

import win32com
import xlwt
import xlrd
from docx import Document
from docx.shared import Inches
from win32com import client as wc
import textract

url = 'http://www.cjhxfund.com/servlet/json'

domain = 'http://www.cjhxfund.com'

version = ''

year_report_path = r'D:\项目\informationDisclosure\src\main\resources\python\year_report'

headers = {
    'Content-Length': '83',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def crawl_notice(fund_code, catalogId, numPerPage):
    body = 'funcNo=904001&catalogId={}&numPerPage={}&isPage=Y&curpage=1&state=3&fundid=' + fund_code
    # body = funcNo=904001&catalogId=1053&numPerPage=10&isPage=Y&curpage=1&state=3&fundid=001662
    r = requests.post(url, data=body.format(catalogId, numPerPage), headers=headers)
    print(r.status_code)
    print(r.text)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return None


# 获取公告
def get_fund_notice(fund_code, catalogId):
    print(fund_code)
    result = crawl_notice(fund_code, catalogId, '1')
    print(result['error_no'])
    if result['error_no'] == '0':
        totalRows = result['results'][0]['totalRows']
        print(totalRows)
        result = crawl_notice(fund_code, catalogId, totalRows)
        print(result['results'][0]['data'])
        return result['results'][0]['data']
    else:
        print('未查询到数据')
        return None


# 获取年报
def get_fund_year_report(notice_list, fund_code):
    for notice in notice_list:
        # if notice['title'].find('年年度报告') >= 0:
        if notice['title'].endswith('年年度报告'):
            print(notice)
            download(domain + notice['link_url'], notice['title'], fund_code)


# 下载文件
def download(url, fileName, fund_code):
    res = requests.get(url)
    dir_path = year_report_path + r'\{}\{}'.format(version, fund_code)
    path = dir_path + r'\{}.{}'.format(fileName, url.split('.')[-1])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(path, "wb") as f:
        f.write(res.content)


# # doc转docx
# def doc_to_docx(path):
#     print('開始轉換格式')
#     word = wc.Dispatch("Word.Application")
#     doc = word.Documents.Open(path)
#     doc.SaveAs(path + 'x', 12)
#     doc.Close()
#     word.Quit()
#     print('結束轉換格式')


# 将 .doc 文件转成 .docx
def doc_to_docx(path):
    print('開始轉換格式')

    os.system('taskkill /im wps.exe')

    # w = wc.Dispatch('kwps application')
    w = wc.Dispatch('Kwps.Application')
    # # w = wc.Dispatch('ket.Application')
    # # w = wc.Dispatch('Word.Application')
    w.Visible = 0
    w.DisplayAlerts = 0
    doc = w.Documents.Open(path)
    newpath = os.path.splitext(path)[0] + '.docx'
    doc.SaveAs(newpath, 12, False, "", True, "", False, False, False, False)
    doc.Close()
    w.Quit()

    # os.remove(path)
    print('結束轉換格式')


# 读取年报
def read_year_report(path):
    # text = textract.process(path)
    # 转换格式
    # doc_to_docx(path)

    list = []

    doc = Document(path)
    year_table = read_spec_table(doc, '11.8 其他重大事件')
    for i in range(len(year_table.rows)):
        if i > 0:
            # for j in range(len(year_table.columns)):
            # print(year_table.cell(i, 1).text)
            # print(year_table.cell(i, 3).text)
            data = {'title': year_table.cell(i, 1).text, 'date': year_table.cell(i, 3).text}
            list.append(data)
    return list


# 读取年报
def read_year_reports(fund_code):
    list = []
    rootdir = year_report_path + r'\{}\{}'.format(version, fund_code)
    file_list = os.listdir(rootdir)
    for i in range(0, len(file_list)):
        path = os.path.join(rootdir, file_list[i])
        if os.path.isfile(path):
            year_report_list = read_year_report(path)
            list.extend(year_report_list)
            # print(path)

    return list


def read_spec_table(document, specText):
    paragraphs = document.paragraphs
    allTables = document.tables
    specText = specText.encode('utf-8').decode('utf-8')
    for aPara in paragraphs:
        # if aPara.text.startswith(specText):
        if aPara.text == specText:
            ele = aPara._p.getnext()
            while (ele.tag != '' and ele.tag[-3:] != 'tbl'):
                ele = ele.getnext()
            if ele.tag != '':
                for aTable in allTables:
                    if aTable._tbl == ele:
                        # for i in range(len(aTable.rows)):
                        #     for j in range(len(aTable.columns)):
                        #         print(aTable.cell(i, j).text)

                        return aTable

    return None


def create_excel(fund_code, fund_name, datas):
    # 新建一个Excel文件（只能通过新建写入）
    data = xlwt.Workbook()
    # 新建一个工作表
    table = data.add_sheet(fund_code, cell_overwrite_ok=True)
    # 写入数据到A1单元格
    # 初始化样式
    style = xlwt.XFStyle()
    style1 = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    # 为样式创建字体
    font = xlwt.Font()
    # 指定字体名字
    font.name = 'Times New Roman'
    # 字体加粗
    font.bold = True
    # 将该font设定为style的字体
    style.font = font
    style.borders = borders
    style1.borders = borders
    # table.write(5, 0, u'Python Excel操作之xlwt创建表格', style)
    tabletitle = ['基金代码', '基金简称', '公告标题', '年度', '披露日期', '公告文件名']

    for i in range(0, len(tabletitle)):
        table.write(0, i, tabletitle[i], style)

    for i in range(0, len(datas)):
        # for j in range(0, len(tableA)):
        table.write(i + 1, 0, fund_code, style1)
        table.write(i + 1, 1, fund_name, style1)
        table.write(i + 1, 2, datas[i]['title'], style1)
        table.write(i + 1, 3, datas[i]['publish_date'].split('-')[0], style1)
        table.write(i + 1, 4, datas[i]['publish_date'].split(' ')[0], style1)
        table.write(i + 1, 5, datas[i]['title'], style1)

    # 注意：如果对同一个单元格重复操作，会引发overwrite Exception，想要取消该功能，需要在添加工作表时指定为可覆盖，像下面这样
    # table=data.add_sheet('name',cell_overwrite_ok=True)
    # 保存文件
    data.save('{}-{}.xls'.format(fund_code, version))
    # 这里只能保存扩展名为xls的，xlsx的格式不支持


def read_excel(fund_code):
    x1 = xlrd.open_workbook('{}-{}.xls'.format(fund_code, version))
    # 2、获取sheet对象
    sheet = x1.sheet_by_name(fund_code)  # 通过sheet名查找
    nrows = sheet.nrows
    # print('表格总行数', nrows)
    # ncols = sheet.ncols
    # print('表格总列数', ncols)
    # row3_values = sheet.row_values(2)
    # print('第3行值', row3_values)
    # col3_values = sheet.col_values(2)
    # print('第3列值', col3_values)
    # cell_3_3 = sheet.cell(2, 2).value
    # print('第3行第3列的单元格的值：', cell_3_3)
    list = []
    for i in range(1, nrows):
        row = sheet.row_values(i)
        # print('第%d行值' % i, row)
        data = {'title': sheet.cell(i, 2).value, 'date': sheet.cell(i, 4).value}
        # print(data)
        list.append(data)
    return list


def compare_aaa(target_list, src_list, ):
    list = []
    for target_data in target_list:
        flag = False
        for src_data in src_list:
            if target_data['title'] == src_data['title'] and target_data['date'] == src_data['date']:
                # print(target_data['title'], src_data['title'])
                # print('存在' + str(target_data))
                flag = True
                break
        else:
            if flag is False:
                print('不存在' + str(target_data))
            continue


if __name__ == '__main__':
    # print(666)
    # version = int(time.time())
    version = '1577017576'
    # notice_list = get_fund_notice('003749', '1052')
    # law_list = get_fund_notice('003749', '1053')
    # get_fund_year_report(notice_list, '003749')
    # create_excel('003749', '创金合信鑫收益A', notice_list + law_list)
    # year_report_list = read_year_reports('003749')
    # print(year_report_list)
    # year_report_list = read_year_report(r'D:\项目\informationDisclosure\src\main\resources\python\year_report\1577017576\003749\创金合信鑫收益灵活配置混合型证券投资基金2017年年度报告.docx')
    # notice_list = read_excel('003749')
    # compare_aaa(year_report_list, notice_list)
    doc_to_docx(r'D:\项目\informationDisclosure\src\main\resources\python\year_report\001662\副本.doc')
