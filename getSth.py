# -*- coding: UTF-8 -*-

import requests
import time
import yaml


with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if config['opinions'][1]['login'] == 'slow':
    from SlowLogin import cookie
else:
    from FastLogin import cookie

COOKIE = cookie()
page_id = 'N305005'
stu_id = config['user'][0]['id']
XNM = '2020'
XQM = ''
TIME = int(round(time.time() * 1000))
URL = f'http://jwxt.cumt.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm={page_id}&su={stu_id}'
sc = {}  # 成绩存储格式 {科目=>[平时分，期末分，总分，学分，绩点]}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Referer': f'http://jwxt.cumt.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm={page_id}&layout=default&su={stu_id}',
    'Cookie': COOKIE
}


def get_detail_scores(_xnm, _xqm, _jxb_id):
    detail_scores_url = f'http://jwxt.cumt.edu.cn//jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm={page_id}&su={stu_id}'
    _data = {
        'xnm': _xnm,
        'xqm': _xqm,
        'jxb_id': _jxb_id,
        '_search': 'false',
        'nd': TIME,
        'queryModel.showCount': '200',
        'queryModel.currentPage': '1',
        'time': 0
    }
    r = requests.post(url=detail_scores_url, headers=headers, data=_data)
    r = r.json()
    _detail_scores = []
    for i in r['items']:
        _detail_scores.append(i['xmcj'])
    return _detail_scores


def getsc():
    data = {
        'xnm': XNM,
        'xqm': XQM,
        '_search': 'false',
        'nd': TIME,
        'queryModel.showCount': 100,
        'queryModel.currentPage': '1',
        'queryModel.sortName': 'jd',
        'queryModel.sortOrder': 'desc',
        'time': 0
    }
    try:
        results = requests.post(url=URL, headers=headers, data=data)
    except:
        print('成绩返回错误')

    results = results.json()
    scores = results['items']
    cnt = results['totalCount']
    print("成绩总数: {}".format(cnt))
    if cnt != 0:
        print('===============正在爬取，请稍后！:)=================')
    for i in scores:
        jxb_id = i['jxb_id']
        xqm = i['xqm']
        xnm = i['xnm']
        detail_scores = get_detail_scores(xnm, xqm, jxb_id)
        detail_scores.append(i['xf'])
        detail_scores.append(i['jd'])
        sc[i['kcmc']] = detail_scores
    return sc


if __name__ == '__main__':
    print(getsc())
    print('================================================')
