# -*- coding: UTF-8 -*-
import os

import requests
import psutil
import base64
import yaml
import jsFunction
from bs4 import BeautifulSoup
from PIL import Image
from OcrApi import generator
import time

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

stu_id = config['user'][0]['id']
stu_password = config['user'][1]['password']

TIME = int(round(time.time() * 1000))
URL = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?time={TIME}'


def password_encode(pwd, sessions):
    url = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time={TIME}&_={TIME-50}'
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


def get_csrftoken(sessions):
    url = f'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html?time={TIME}'
    r = sessions.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.find('input', attrs={'id': 'csrftoken'}).attrs['value']
    return token


def get_code_by_people(sessions):
    header_code = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    url = f'http://jwxt.cumt.edu.cn/jwglxt/kaptcha?time={TIME}'
    request = sessions.get(url, headers=header_code)
    path = './image/code.jpg'
    with open(path, 'wb')as code_img:
        code_img.write(request.content)
    code_img = Image.open(path)
    process_list = []
    for proc in psutil.process_iter():
        process_list.append(proc)
    code_img.show()
    code = input("请输入验证码:\n")
    for proc in psutil.process_iter():
        if not proc in process_list:
            proc.kill()
    os.remove(path)
    return code


def get_code_by_ocr(sessions):
    header_code = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    url = f'http://jwxt.cumt.edu.cn/jwglxt/kaptcha?time={TIME}'
    request = sessions.get(url, headers=header_code)
    path = './image/yzm.png'
    with open(path, 'wb')as code_img:
        code_img.write(request.content)
    code = generator(path)
    return code


def login():
    sessions = requests.Session()
    token = get_csrftoken(sessions)
    pwd_enc = password_encode(stu_password, sessions)
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
    # 智能人工识别验证码
    if config['opinions'][0]['AI']:
        code = get_code_by_ocr(sessions)
    else:
        code = get_code_by_people(sessions)
    # 人工智能识别验证码
    data = {
        'csrftoken': token,
        'language':  'zh_CN',
        'yhm': stu_id,
        'mm': pwd_enc,
        'mm': pwd_enc,
        'yzm': code
    }
    ret = sessions.post(url=URL, headers=headers, data=data)
    cookies = sessions.cookies.get_dict()
    return ret, cookies


def cookie():
    rt = login()
    while rt[0].text.find('验证码输入错误') != -1:
        print('验证码输入错误:)')
        rt = login()
    cookies = 'JSESSIONID='+rt[1]['JSESSIONID']+'; X-LB='+rt[1]['X-LB']
    return cookies


if __name__ == '__main__':
    test = login()
    print(test[1])
    while test[0].text.find('验证码输入错误') != -1:
        print('验证码输入错误:)')
        test = login()
