from datetime import *
import sys
import requests
import yaml

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

def log(content):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(content))
    sys.stdout.flush()

def sendMessage(_title, _content):
    _url = f'https://sctapi.ftqq.com/{Server_address}.send'
    _data = {
        'title': _title,
        'desp': _content,
    }
    try:
        requests.post(url=_url, data=_data)
    except:
        pass

id = config['user'][0]['id']
pwd = config['user'][1]['password']
Server_address = config['api'][2]['server']