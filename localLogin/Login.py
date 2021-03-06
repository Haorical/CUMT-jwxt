# -*- encoding: utf-8 -*-
'''
@File    :   Login.py
@Time    :   2022/05/21 23:47:17
@Author  :   haorical
@Version :   1.1
@Contact :   haorical@outlook.com
'''
import os
import requests
import psutil
import base64
import localLogin.jsFunction as jsFunction
from bs4 import BeautifulSoup
from PIL import Image
import time
from moudles.ext import log, generator, AI, print_login


class FastLogin:

    def __init__(self, _id, _pwd):
        print_login()
        self.stu_id = _id
        self.stu_password = _pwd
        self.TIME = int(round(time.time() * 1000))
        self.sessions = requests.Session()

    def password_encode(self, pwd, sessions):
        url = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time={self.TIME}&_={self.TIME - 50}'
        ret = sessions.get(url)
        ret = ret.json()
        modulus = ret['modulus']
        exponent = ret['exponent']
        _modulus = base64.b64decode(modulus).hex()
        _exponent = base64.b64decode(exponent).hex()
        rsa = jsFunction.RSAKey()
        rsa.setPublic(_modulus, _exponent)
        pwd_rsa = rsa.encrypt(pwd)
        pwd_byte = bytes.fromhex(pwd_rsa)
        pwd_cry = base64.b64encode(pwd_byte).decode('utf-8')
        return pwd_cry

    def get_csrftoken(self, sessions):
        url = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?time={self.TIME}'
        try:
            r = sessions.get(url)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')
            token = soup.find('input', attrs={'id': 'csrftoken'}).attrs['value']
        except:
            log('csrf获取失败!')
            exit(1)
        return token

    def get_code_by_people(self, sessions):
        header_code = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
        }
        url = f'http://jwxt.cumt.edu.cn/jwglxt/kaptcha?time={self.TIME}'
        request = sessions.get(url, headers=header_code)
        path = './image/code.jpg'
        with open(path, 'wb')as code_img:
            code_img.write(request.content)
        code_img = Image.open(path)
        process_list = []
        for proc in psutil.process_iter():
            process_list.append(proc)
        code_img.show()
        log("请输入验证码:")
        code = input()
        try:
            for proc in psutil.process_iter():
                if not proc in process_list:
                    proc.kill()
        except:
            pass
        os.remove(path)
        return code

    def get_code_by_ocr(self, sessions):
        log("开始识别验证码！")
        header_code = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
        }
        url = f'http://jwxt.cumt.edu.cn/jwglxt/kaptcha?time={self.TIME}'
        request = sessions.get(url, headers=header_code)
        path = './image/yzm.png'
        with open(path, 'wb')as code_img:
            code_img.write(request.content)
        code = generator(path)
        return code

    def login(self):
        token = self.get_csrftoken(self.sessions)
        pwd_enc = self.password_encode(self.stu_password, self.sessions)
        URL = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?time={self.TIME}'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'close',
            'Content-Length': '482',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jwxt.cumt.edu.cn',
            'Origin': 'http: // jwxt.cumt.edu.cn',
            'Referer': 'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        # 智能人工识别
        if AI:
            code = self.get_code_by_ocr(self.sessions)
        else:
            code = self.get_code_by_people(self.sessions)
        # 人工智能识别
        data = {
            'csrftoken': token,
            'language': 'zh_CN',
            'yhm': self.stu_id,
            'mm': pwd_enc,
            'mm': pwd_enc,
            'yzm': code
        }
        ret = self.sessions.post(url=URL, headers=headers, data=data)
        cookies = self.sessions.cookies.get_dict()
        return ret, cookies

    def get_status(self):
        log("开始模拟登录！")
        rt = self.login()
        # print(rt)
        while rt[0].text.find('验证码输入错误') != -1:
            log('验证码识别错误，正在尝试重新登录！')
            rt = self.login()
        if 'route' in rt[1]:
            cookies = 'JSESSIONID=' + rt[1]['JSESSIONID'] + '; X-LB=' + rt[1]['X-LB'] + '; route=' + rt[1]['route']
        else:
            cookies = 'JSESSIONID=' + rt[1]['JSESSIONID'] + '; X-LB=' + rt[1]['X-LB']
        log("模拟登录成功！")
        return cookies, self.sessions

# if __name__ == '__main__':
#     stu_id = config['user'][0]['id']
#     stu_password = config['user'][1]['password']
#     test = FastLogin(stu_id, stu_password)
#     print(test.cookie())
