# -*- encoding: utf-8 -*-
'''
@File    :   getSth.py
@Time    :   2022/05/21 23:47:34
@Author  :   haorical
@Version :   1.1
@Contact :   haorical@outlook.com
'''

import requests
import time
from ext import log, config
from Login import FastLogin

class Stu:

    def __init__(self, _stu_id, _stu_pwd):
        self.stu_id = _stu_id
        self.stu_pwd = _stu_pwd
        self.cookie = self.get_cookies()

    def get_cookies(self):
        cookies = FastLogin(self.stu_id, self.stu_pwd).cookie() 
        return cookies
       
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

    def getScores(self, xnm, xqm=''):
        # 成绩存储格式 {科目=>[平时分，期末分，总分，学分，绩点]}
        log('开始获取成绩信息！')
        sc = {}
        TIME = int(round(time.time() * 1000))
        XNM = xnm
        XQM = xqm
        URL = f'http://jwxt.cumt.edu.cn//jwglxt/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su={self.stu_id}'
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

        # print(res.text)

        results = res.json()
        scores = results['items']
        cnt = results['totalCount']
        print("成绩总数: {}".format(cnt))
        if cnt != 0:
            pass
            # print('===============正在爬取，请稍后！:)=================')
        for i in scores:
            jxb_id = i['jxb_id']
            xqm = i['xqm']
            xnm = i['xnm']
            detail_scores = self.get_detail_scores(xnm, xqm, jxb_id, headers, TIME)
            detail_scores.append(i['xf'])
            detail_scores.append(i['jd'])
            sc[i['kcmc']] = detail_scores
        return sc

    def getCourses(self, xnm, xqm=''):
        log("开始获取课表信息！")
        url = f'http://jwxt.cumt.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508&&su={self.stu_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Referer': f'http://jwxt.cumt.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su={self.stu_id}',
            'Cookie': self.cookie
        }
        data = {
            'xnm': xnm,
            'xqm': xqm,
            'kzlx': 'ck'
        }
        try:
            res = requests.post(url=url, headers=headers, data=data)
        except:
            log('课表查询失败')
            exit(1)
        data = res.json()

        log(data['kbList'][18]['jxbmc'])


# if __name__ == '__main__':
#     stu_id = config['user'][0]['id']
#     stu_password = config['user'][1]['password']
#     cookies = FastLogin(stu_id, stu_password).cookie()
#     # print(cookies)
#     test = Person(stu_id, cookies, 2021, )
#     test.getScores()

