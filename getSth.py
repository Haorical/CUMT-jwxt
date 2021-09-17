# -*- coding: UTF-8 -*-

import requests
import time
import sys
import yaml
from datetime import datetime, timedelta, timezone

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if config['opinions'][1]['login'] == 'slow':
    from SlowLogin import Login
else:
    from FastLogin import Login


def log(content):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(content))
    sys.stdout.flush()


class Person:

    def __init__(self, _stu_id, _stu_password, _xnm, _xqm=''):
        self.stu_id = _stu_id
        self.stu_password = _stu_password
        self.cookie = Login(self.stu_id, self.stu_password).cookie()
        self.xnm = _xnm
        self.xqm = _xqm

    def get_detail_scores(self, __xnm, __xqm, __jxb_id, __headers, __time):
        detail_scores_url = f'http://jwxt.cumt.edu.cn//jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305005&su={self.stu_id}'
        _data = {
            'xnm': __xnm,
            'xqm': __xqm,
            'jxb_id': __jxb_id,
            '_search': 'false',
            'nd': __time,
            'queryModel.showCount': '200',
            'queryModel.currentPage': '1',
            'time': 0
        }
        r = requests.post(url=detail_scores_url, headers=__headers, data=_data)
        r = r.json()
        _detail_scores = []
        for i in r['items']:
            _detail_scores.append(i['xmcj'])
        return _detail_scores

    def getScores(self):
        # 成绩存储格式 {科目=>[平时分，期末分，总分，学分，绩点]}
        log('开始获取成绩信息！')
        sc = {}
        TIME = int(round(time.time() * 1000))
        XNM = self.xnm
        XQM = self.xqm
        URL = f'http://jwxt.cumt.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005&su={self.stu_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Referer': f'http://jwxt.cumt.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su={self.stu_id}',
            'Cookie': self.cookie
        }
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
            res = requests.post(url=URL, headers=headers, data=data)
        except:
            log('成绩查询失败')
            exit(1)

        results = res.json()
        scores = results['items']
        cnt = results['totalCount']
        print("成绩总数: {}".format(cnt))
        if cnt != 0:
            print('===============正在爬取，请稍后！:)=================')
        for i in scores:
            jxb_id = i['jxb_id']
            xqm = i['xqm']
            xnm = i['xnm']
            detail_scores = self.get_detail_scores(xnm, xqm, jxb_id, headers, TIME)
            detail_scores.append(i['xf'])
            detail_scores.append(i['jd'])
            sc[i['kcmc']] = detail_scores
        return sc

    def getCourses(self):
        log("开始获取课表信息！")
        url = f'http://jwxt.cumt.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508&&su={self.stu_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Referer': f'http://jwxt.cumt.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su={self.stu_id}',
            'Cookie': self.cookie
        }
        data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
            'kzlx': 'ck'
        }
        try:
            res = requests.post(url=url, headers=headers, data=data)
        except:
            log('课表查询失败')
            exit(1)
        data = res.json()

        log(data['kbList'][18]['jxbmc'])


if __name__ == '__main__':
    stu_id = config['user'][0]['id']
    stu_password = config['user'][1]['password']
    test = Person(stu_id, stu_password, 2021, 1)
    test.getCourses()
