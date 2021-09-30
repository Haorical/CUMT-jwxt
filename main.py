# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/09/30 19:04:55
@Author  :   haorical
@Version :   1.0
@Contact :   haorical@outlook.com
'''
import yaml
import uuid
import requests
from getSth import Person

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == '__main__':
    api = config['api']
    stu_id = config['user'][0]['id']
    stu_password = config['user'][1]['password']
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    mac_address = '-'.join([mac_address[i:i + 2] for i in range(0, 11, 2)])
    data = {
        'username': stu_id,
        'password': stu_password,
        'key': api[1]['key'],
        'mac': mac_address
    }

    cookies = requests.post(url=api[0]['url'], data=data).text

    if cookies.find('KeyError') != -1:
        print('key错误，请联系开发者获取')
        exit(1)

    # 学号 密码 学年 学期(缺省)
    user = Person(stu_id, cookies, 2020)

    print(user.getScores())
