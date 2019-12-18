import requests

url = 'http://www.cjhxfund.com/servlet/json'

headers = {
    'Content-Length': '83',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def get_fund_notice(fund_code):
    print(fund_code)
    body = 'funcNo=904001&catalogId=1052&numPerPage=10&isPage=Y&curpage=1&state=3&fundid=001662'
    # body = funcNo=904001&catalogId=1053&numPerPage=10&isPage=Y&curpage=1&state=3&fundid=001662
    r = requests.post(url, data=body, headers=headers)
    print(r.text)


if __name__ == '__main__':
    print(666)
    get_fund_notice(777)
