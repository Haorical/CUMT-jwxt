from datetime import *
import sys
import requests
import yaml
import os
import ddddocr
import onnxruntime

onnxruntime.set_default_logger_severity(3)

# 读配置
with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# 打印调试信息
def log(content):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(content))
    sys.stdout.flush()


# server酱
def sendMessage(_title, _content):
    _url = f'https://sctapi.ftqq.com/{SERVER_ADDRESS}.send'
    _data = {
        'title': _title,
        'desp': _content,
    }
    try:
        requests.post(url=_url, data=_data)
    except:
        pass


# ocr模块
def generator(path):
    onnxruntime.set_default_logger_severity(3)
    with open(path, 'rb') as f:
        img_bytes = f.read()
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(img_bytes)
    os.remove(path)
    return code


def print_login():
    print(
        """
 __          __  _                            _                           ______        _   _                 _       
 \ \        / / | |                          | |                         |  ____|      | | | |               (_)      
  \ \  /\  / ___| | ___ ___  _ __ ___   ___  | |_ ___    _   _ ___  ___  | |__ __ _ ___| |_| |     ___   __ _ _ _ __  
   \ \/  \/ / _ | |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | | | / __|/ _ \ |  __/ _` / __| __| |    / _ \ / _` | | '_ \ 
    \  /\  |  __| | (_| (_) | | | | | |  __/ | || (_) | | |_| \__ |  __/ | | | (_| \__ | |_| |___| (_) | (_| | | | | |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \__,_|___/\___| |_|  \__,_|___/\__|______\___/ \__, |_|_| |_|
                                                                                                         __/ |        
                                                                                                        |___/         
                                                                                                        by haorical
"""
    )


def print_rob():
    print(
        """
  _____       _       _____                         _             _    _                  _           _ 
 |  __ \     | |     |  __ \                       | |           | |  | |                (_)         | |
 | |__) |___ | |__   | |  | | ___ _ __ ___   ___   | |__  _   _  | |__| | __ _  ___  _ __ _  ___ __ _| |
 |  _  // _ \| '_ \  | |  | |/ _ \ '_ ` _ \ / _ \  | '_ \| | | | |  __  |/ _` |/ _ \| '__| |/ __/ _` | |
 | | \ \ (_) | |_) | | |__| |  __/ | | | | | (_) | | |_) | |_| | | |  | | (_| | (_) | |  | | (_| (_| | |
 |_|  \_\___/|_.__/  |_____/ \___|_| |_| |_|\___/  |_.__/ \__, | |_|  |_|\__,_|\___/|_|  |_|\___\__,_|_|
                                                           __/ |                                        
                                                          |___/                                         
"""
    )


ID = config['user'][0]['id']
PWD = config['user'][1]['password']
SERVER_ADDRESS = config['api'][2]['server']
AI = config['opinions'][0]['AI']
HOST = config['opinions'][1]['host']
