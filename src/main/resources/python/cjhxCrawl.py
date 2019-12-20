import requests
import xlwt

url = 'http://www.cjhxfund.com/servlet/json'

headers = {
    'Content-Length': '83',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def get_fund_notice(fund_code):
    print(fund_code)
    body = 'funcNo=904001&catalogId=1052&numPerPage=157&isPage=Y&curpage=1&state=3&fundid=001662'
    # body = funcNo=904001&catalogId=1053&numPerPage=10&isPage=Y&curpage=1&state=3&fundid=001662
    r = requests.post(url, data=body, headers=headers)
    print(r.text)


def create_excel(datas):
    # 新建一个Excel文件（只能通过新建写入）
    data = xlwt.Workbook()
    # 新建一个工作表
    table = data.add_sheet('name')
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
    table.write(5, 0, u'Python Excel操作之xlwt创建表格', style)
    tabletitle = ['姓名', '年龄', '职业']
    tableA = ['张三', '李四', '王五', '麻子']
    tableB = ['30', '28', '18', '26']
    tableC = ['工程师', '学生', '学生', '老师']
    for i in range(0, len(tabletitle)):
        table.write(0, i, tabletitle[i], style)
    for j in range(0, len(tableA)):
        table.write(j + 1, 0, tableA[j], style1)
    for k in range(0, len(tableB)):
        table.write(k + 1, 1, tableB[k], style1)
    for l in range(0, len(tableC)):
        table.write(l + 1, 2, tableC[l], style1)
    # 注意：如果对同一个单元格重复操作，会引发overwrite Exception，想要取消该功能，需要在添加工作表时指定为可覆盖，像下面这样
    # table=data.add_sheet('name',cell_overwrite_ok=True)
    # 保存文件
    data.save('test.xls')
    # 这里只能保存扩展名为xls的，xlsx的格式不支持


if __name__ == '__main__':
    print(666)
    get_fund_notice(777)
    create_excel(None)
