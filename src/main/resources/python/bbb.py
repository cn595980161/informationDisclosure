import os
import pandas as pd
import difflib
import xlsxwriter


def compare_aaa(target_list, src_list):
    _list = []
    # 1. 过滤存在的信息
    # 临时列表
    _target_list = target_list[:]
    for target_data in _target_list:
        # 临时列表
        _src_list = src_list[:]
        for src_data in _src_list:
            # 一致
            if target_data[1] == src_data[0] and target_data[0] == src_data[1]:
                # flag = True
                print('一致', target_data)
                target_list.remove(target_data)
                src_list.remove(src_data)
                break
        else:
            continue

    # 2.找出不存在的信息
    for target_data in target_list:
        date_diff = False
        similar_ratio = float()
        tmp_src_data = {}

        # 过滤不存在的
        for src_data in src_list:

            # 披露时间不一致
            if target_data[1] == src_data[0] and target_data[0][:4] == src_data[1][:4] and target_data[0][5:] != src_data[1][5:]:
                print('披露时间不一致情况:', target_data, src_data)
                data = target_data
                data.append(src_data[0])
                data.append(src_data[1])
                data.append(True)
                data.append([])
                _list.append(data)
                break

            # # 相似度比较
            # _similar_ratio = string_similar(target_data[1], src_data[0])
            # if (_similar_ratio > similar_ratio) and (_similar_ratio < 1.0) and (_similar_ratio >= 0.7) and target_data[0][:4] == src_data[1][:4]:
            #     similar_ratio = _similar_ratio
            #     tmp_src_data = src_data

        else:
            print('不一致' + str(target_data))
            data = target_data
            if tmp_src_data == {}:
                data.append('')
                data.append('')
                data.append(date_diff)
                data.append([])
                data.append(0)
            else:
                print(666)
                # differences = list(difflib.Differ().compare(target_data[1], tmp_src_data[0]))
                # print('不一致情况:', str(similar_ratio), "".join(differences))
                #
                # data.append(tmp_src_data[0])
                # data.append(tmp_src_data[1])
                # data.append(date_diff)
                # data.append(differences)
                # data.append(similar_ratio)

            _list.append(data)
            continue

    return _list


def create_diff_excel(datas):
    # 新建一个Excel文件
    workbook = xlsxwriter.Workbook('报社公告不一致.xlsx')
    # 新建一个工作表
    worksheet = workbook.add_worksheet()

    default_format = workbook.add_format()
    red_format = workbook.add_format({'font_color': 'red'})
    green_format = workbook.add_format({'font_color': 'green'})
    title_format = workbook.add_format({'bold': True})

    # table.write(5, 0, u'Python Excel操作之xlwt创建表格', style)
    tabletitle = ['报社公告标题', '报社披露日期', '公告标题', '披露日期']

    for i in range(0, len(tabletitle)):
        worksheet.write(0, i, tabletitle[i], title_format)

    for i in range(0, len(datas)):
        # for j in range(0, len(tableA)):
        print(datas[i])
        worksheet.write_string(i + 1, 0, datas[i][1])
        worksheet.write_string(i + 1, 1, datas[i][0])
        worksheet.write_string(i + 1, 2, datas[i][3])
        worksheet.write_string(i + 1, 3, datas[i][4])

    workbook.close()


def string_similar(s1, s2):
    return difflib.SequenceMatcher(lambda x: x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], s1, s2).ratio()


def red_fund(file_path):
    dfs = []
    for file in os.listdir(file_path):
        if os.path.splitext(file)[1] in ['.xls']:
            # print(file)

            # 依次读取多个相同结构的Excel文件并创建DataFrame
            dfs.append(pd.read_excel(file_path + '\\' + file, usecols=[17, 12, 21], converters={u'fund_code': str}))
    # 将多个DataFrame合并为一个
    df = pd.concat(dfs)
    # # 写入Excel文件，不包含索引数据
    # df.to_excel('result.xlsx', index=False)
    notice_list = df.values.tolist()
    print(notice_list)
    return notice_list


if __name__ == '__main__':
    # paper_list = pd.read_csv(r'D:\项目\informationDisclosure\src\main\resources\python\喵喵喵.csv', names=['date', 'title', 'source'])
    paper_list = pd.read_csv(r'D:\项目\informationDisclosure\src\main\resources\python\喵喵喵.csv')
    # for ir in paper_list.itertuples():
    #     print(ir[1], ir[2], ir[3])
    paper_list = paper_list.values.tolist()
    # print(paper_list)
    #
    #
    #
    # compare_aaa(paper_list,)

    notice_list = red_fund('E:\info_notice')
    diff = compare_aaa(paper_list, notice_list)
    create_diff_excel(diff)
