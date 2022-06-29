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
from moudles.ext import ID,PWD,log
from localLogin.Login import FastLogin

class Stu:
    def __init__(self, _stu_id, _stu_pwd):
        self.stu_id = _stu_id
        self.stu_pwd = _stu_pwd
        self.cookie = None
        self.session = None
        self.slogin()
        self._time = int(round(time.time() * 1000))

    def slogin(self):
        try:
            ts = FastLogin(self.stu_id, self.stu_pwd).get_status()
            # print(ts)
            self.cookie = ts[0]
            self.session = ts[1]
            return True
        except:
            log('登录失败!')
            return False
    
    def get_cookie(self):
        return self.cookie

    def get_session(self):
        return self.session

    def get_detail_scores(self, __xnm, __xqm, __jxb_id, __headers):
        detail_scores_url = f'http://jwxt.cumt.edu.cn//jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305005&su={self.stu_id}'
        _data = {
            'xnm': __xnm,
            'xqm': __xqm,
            'jxb_id': __jxb_id,
            '_search': 'false',
            'nd': self._time,
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

    def getScores(self, _xnm, _xqm=''):
        log('开始获取成绩信息！')
        sc = {}
        TIME = self._time
        XNM = _xnm
        XQM = _xqm
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
        log('成绩查询成功!')
        # print(res.text)

        results = res.json()
        scores = results['items']
        cnt = results['totalCount']
        print("成绩总数: {}".format(cnt))
        if cnt != 0:
            pass
        for i in scores:
            jxb_id = i['jxb_id']
            xqm = i['xqm']
            xnm = i['xnm']
            detail_scores = self.get_detail_scores(xnm, xqm, jxb_id, headers)
            detail_scores.append(i['xf'])
            detail_scores.append(i['jd'])
            sc[i['kcmc']] = detail_scores
        return sc

    def getCourses(self, xnm, xqm=3):
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

        # print(data)
    def do_judge(self):
        log('开始请求评价！')
        TIME = self._time
        URL = f'http://jwxt.cumt.edu.cn/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=query&gnmkdm=N401605&su={self.stu_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Referer': f'http://jwxt.cumt.edu.cn/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=details&gnmkdm=N401605&layout=default&su={self.stu_id}',
            'Cookie': self.cookie
        }
        data = {
                "_search": "false",
                "nd": TIME,
                "queryModel.showCount": "5",
                "queryModel.currentPage": "1",
                "queryModel.sortName": "",
                "queryModel.sortOrder": "asc",
                "time": "0"
        }
        try:
            res = requests.post(url=URL, headers=headers, data=data)
        except:
            log('请求评价失败')
        log('评价查询成功!')
        full_data = res.json()
        items = full_data['items'][0]
        print(items)
        # scores = results['items']
        # cnt = results['totalCount']
        # print("成绩总数: {}".format(cnt))
        # if cnt != 0:
        #     pass
        # for i in scores:
        #     jxb_id = i['jxb_id']
        #     xqm = i['xqm']
        #     xnm = i['xnm']
        #     detail_scores = self.get_detail_scores(xnm, xqm, jxb_id, headers)
        #     detail_scores.append(i['xf'])
        #     detail_scores.append(i['jd'])
        #     sc[i['kcmc']] = detail_scores
        # return sc


if __name__ == '__main__':
    test = Stu(ID,PWD)
    test.do_judge()

