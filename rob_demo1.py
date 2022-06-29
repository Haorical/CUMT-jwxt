# -*- encoding: utf-8 -*-
'''
@File    :   rob.py
@Time    :   2022/06/01 12:34:50
@Author  :   haorical
@Version :   1.0
@Contact :   haorical@outlook.com
'''

from urllib.parse import quote
import HackRequests
from moudles.ext import *
from getSth import Stu
import json

stu = Stu(ID, PWD)

cookie = stu.get_cookie()

hack = HackRequests.hackRequests()

def get_all_classes_info():
    raw1 = f"""
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su={ID} HTTP/1.1
Host: jwxt.cumt.edu.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 388
Origin: http://jwxt.cumt.edu.cn
Connection: close
Referer: http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={ID}
Cookie: {cookie}

rwlx=2&xkly=0&bklx_id=0&sfkkjyxdxnxq=0&xqh_id=2&jg_id=08&njdm_id_1=2020&zyh_id_1=0840&zyh_id=0840&zyfx_id=wfx&njdm_id=2020&bh_id=201084003&xbm=1&xslbdm=wlb&mzm=01&xz=4&ccdm=3&xsbj=4294967296&sfkknj=0&sfkkzy=0&kzybkxy=0&sfznkx=0&zdkxms=0&sfkxq=1&sfkcfx=0&kkbk=0&kkbkdj=0&sfkgbcx=0&sfrxtgkcxd=0&tykczgxdcs=0&xkxnm=2021&xkxqm=12&kklxdm=18&bbhzxjxb=0&rlkz=0&xkzgbj=0&kspage=1&jspage=10&jxbzb=    
"""


def get_class_info(kcid):
    # tmp_list
    raw1 = f"""
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su={ID} HTTP/1.1
Host: jwxt.cumt.edu.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 418
Origin: http://jwxt.cumt.edu.cn
Connection: close
Referer: http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={ID}
Cookie: {cookie}

filter_list%5B0%5D={kcid}&rwlx=2&xkly=0&bklx_id=0&sfkkjyxdxnxq=0&xqh_id=2&jg_id=08&njdm_id_1=2020&zyh_id_1=0840&zyh_id=0840&zyfx_id=wfx&njdm_id=2020&bh_id=201084003&xbm=1&xslbdm=wlb&mzm=01&xz=4&ccdm=3&xsbj=4294967296&sfkknj=0&sfkkzy=0&kzybkxy=0&sfznkx=0&zdkxms=0&sfkxq=1&sfkcfx=0&kkbk=0&kkbkdj=0&sfkgbcx=0&sfrxtgkcxd=0&tykczgxdcs=0&xkxnm=2021&xkxqm=12&kklxdm=18&bbhzxjxb=0&rlkz=0&xkzgbj=0&kspage=1&jspage=10&jxbzb=
"""
    raw2 = f"""
POST /jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su={ID} HTTP/1.1
Host: jwxt.cumt.edu.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 438
Origin: http://jwxt.cumt.edu.cn
Connection: close
Referer: http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={ID}
Cookie: {cookie}

filter_list%5B0%5D={kcid}&rwlx=2&xkly=0&bklx_id=0&sfkkjyxdxnxq=0&xqh_id=2&jg_id=08&zyh_id=0840&zyfx_id=wfx&njdm_id=2020&bh_id=201084003&xbm=1&xslbdm=wlb&mzm=01&xz=4&bbhzxjxb=0&ccdm=3&xsbj=4294967296&sfkknj=0&sfkkzy=0&kzybkxy=0&sfznkx=0&zdkxms=0&sfkxq=1&sfkcfx=0&kkbk=0&kkbkdj=0&xkxnm=2021&xkxqm=12&xkxskcgskg=0&rlkz=0&kklxdm=18&kch_id=DDA352C6ADDC801AE0531F70A8C00B9C&jxbzcxskg=0&xkkz_id=DFF8AF02B868C55FE0531E70A8C06109&cxbj=0&fxbj=0
"""
    h1 = hack.httpraw(raw1).text()
    h2 = hack.httpraw(raw2).text()
    dt1 = json.loads(h1)
    dt2 = json.loads(h2)
    rt = {}
    dt1 = dt1['tmpList'][0]
    dt2 = dt2[0]
    rt['jxb_ids'] = dt2['do_jxb_id']
    rt['kch_id'] = dt1['kch_id']
    rt['kcmc'] = "("+str(kcid)+")"+quote(dt1['kcmc'])+f"+-+{dt1['xf']}+"+quote('学分')
    rt['xxkbj'] = dt1['xxkbj']
    rt['cxbj'] = dt1['cxbj']
    rt['kklxdm'] = dt1['kklxdm']
    return rt


def _callback(r:HackRequests.response):
    # 从回调函数取出结果，参数r是response结果
    if '成功' in r.text:
        sendMessage('选课成功','hahahahhahaha')
        exit(0)
    print(r.text())


def rob(kcid):
    dt = {}
    while 1:
        try:
            dt = get_class_info(kcid)
        except:
            log('重新获取课程信息')
            pass
        if dt:
            break
    raw1 = f"""
POST /jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512&su={ID} HTTP/1.1
Host: jwxt.cumt.edu.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 588
Origin: http://jwxt.cumt.edu.cn
Connection: close
Referer: http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={ID}
Cookie: {cookie}

jxb_ids={dt['jxb_ids']}&kch_id={dt['kch_id']}&kcmc={dt['kcmc']}&rwlx=2&rlkz=0&rlzlkz=1&sxbj=1&xxkbj={dt['xxkbj']}&qz=0&cxbj={dt['cxbj']}&xkkz_id=DFF8AF02B868C55FE0531E70A8C06109&njdm_id=2020&zyh_id=0840&kklxdm={dt['kklxdm']}&xklc=3&xkxnm=2021&xkxqm=12
"""
    threadpool = HackRequests.threadpool(threadnum=100,callback=_callback,timeout=10)
    for i in range(100000):
        threadpool.httpraw(raw=raw1)
    threadpool.run()

