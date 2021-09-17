# -*- coding: UTF-8 -*-
import time
import yaml
from selenium import webdriver
from OcrApi import generator

with open('./config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

stu_id = config['user'][0]['id']
stu_password = config['user'][1]['password']

driver = webdriver.Chrome()

url = 'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html'
driver.get(url)

driver.find_element_by_xpath('//*[@id="yhm"]').send_keys(stu_id)
driver.find_element_by_xpath('//*[@id="mm"]').send_keys(stu_password)
code_image = driver.find_element_by_xpath('//*[@id="yzmPic"]')
path = './image/yzm.png'
code_image.screenshot(path)
yzm = generator(path)
driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(yzm)
driver.find_element_by_xpath('//*[@id="dl"]').click()


def cookie():
    time.sleep(0.1)
    cookies = driver.get_cookies()
    print(cookies)
    driver.quit()
    cookies = cookies[1]['name']+'='+cookies[1]['value']  # +'; X-LB='+cookie[0]['value']
    return cookies

