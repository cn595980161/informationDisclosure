import os
import re
from shutil import copy

import pandas as pd

report_path = r'D:\info_report'
notice_path = r'D:\info_notice'


def auto_fill_merge_cell(df):
    cols = [
        c
        for c in df.columns
        if pd.api.types.is_string_dtype(df[c])
    ]

    df[cols] = df[cols].ffill()


def match_str(v, s):
    # reg = ''
    for reg in v:
        if reg[-1:] != '-':
            reg = reg
            if not re.search(reg, s):
                return False
        elif reg.endswith('-'):
            reg = reg[:-1]
            if re.search(reg, s):
                return False
        elif reg == '无':
            return False
    return True


def save_file(rule, data):
    root_path = os.path.join(report_path, str(data['年度']), str(rule[0]), str(rule[1]))
    # 不存在创建
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    print(os.getcwd())
    file_path = os.path.join(notice_path, '1577779898', str(data['基金代码']))
    copy(file_path + '\\' + data['公告文件名'], root_path)
    # 复制文件


if __name__ == '__main__':
    # print(re.search('招募说明书|更新+', '创金合信沪港深研究精选灵活配置混合型证券投资基金招募说明书（更新）摘要（2019年第2号）'))
    notic_data = pd.read_excel(r'D:\项目\informationDisclosure\src\main\resources\python\notice\1577851436\001662.xls', sheet_name='001662', converters={u'基金代码': str})
    # for row in range(0, notic_data.shape[0]):
    #     print(notic_data.iloc[row][2])

    rule_data = pd.read_excel(r'C:\Users\Administrator\Desktop\信批文件分类规则.xlsx', sheet_name='分门别类规则')
    auto_fill_merge_cell(rule_data)
    # print(rule_data)
    for row in range(0, rule_data.shape[0]):
        # print(rule_data.iloc[row][2])
        rule = rule_data.iloc[row][2].split(',')
        # print(rule)
        for row1 in range(0, notic_data.shape[0]):
            # print(notic_data.iloc[row1][2])
            title = notic_data.iloc[row1][2]
            file_name = notic_data.iloc[row1][5]
            if not file_name.endswith('.') and match_str(rule, title):
                print(rule_data.iloc[row])
                print(title)
                save_file(rule_data.iloc[row], notic_data.iloc[row1])
