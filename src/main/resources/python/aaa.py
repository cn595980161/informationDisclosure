import pandas as pd


def auto_fill_merge_cell(df):
    cols = [
        c
        for c in df.columns
        if pd.api.types.is_string_dtype(df[c])
    ]

    df[cols] = df[cols].ffill()


def in_str(v, s):
    for a in v:
        if a in s:
            return True
    return False


notic_data = pd.read_excel(r'D:\项目\informationDisclosure\src\main\resources\python\notice\1577368698\001199.xls', sheet_name='001199')
# for row in range(0, notic_data.shape[0]):
#     print(notic_data.iloc[row][2])

rule_data = pd.read_excel(r'C:\Users\Administrator\Desktop\信批文件分类规则.xlsx', sheet_name='分门别类规则')
auto_fill_merge_cell(rule_data)
# print(rule_data)
for row in range(0, rule_data.shape[0]):
    # 取每一行的2-66列数据，注意下面这个取法最后是带列头的字典形式
    # print(rule_data.iloc[row][2])
    rule = rule_data.iloc[row][2].split(',')
    # print(rule)
    for row1 in range(0, notic_data.shape[0]):
        # print(notic_data.iloc[row1][2])
        title = notic_data.iloc[row1][2]
        if in_str(rule, title):
            print(666)
            print(title)
