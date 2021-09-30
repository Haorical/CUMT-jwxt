# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2021/09/30 16:33:58
@Author  :   haorical
@Version :   1.0
@Contact :   haorical@outlook.com
'''
from time import sleep
import yaml
import sys
import threading
from datetime import datetime, timedelta, timezone
from main import test
with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

print(config['user'][0]['id'])

def log(content):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(content))
    sys.stdout.flush()

class Thread(threading.Thread):
    def __init__(self, __id):
        threading.Thread.__init__(self)
        self.id = __id
    def run(self):
        log(self.id)
        test()
        return super().run()

threads = []
for i in range(0,200):
    threads.append(Thread(i))

for t in threads:
    t.start()

t.join()
