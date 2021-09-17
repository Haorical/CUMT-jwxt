# -*- coding: UTF-8 -*-
import yaml
from getSth import Person

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == '__main__':
    stu_id = config['user'][0]['id']
    stu_password = config['user'][1]['password']
    user = Person(stu_id, stu_password, 2020)
    print(user.getScores())