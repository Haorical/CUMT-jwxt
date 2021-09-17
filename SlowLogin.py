# -*- coding: UTF-8 -*-
import time
from selenium import webdriver
from OcrApi import generator


class Login:

    def __init__(self, _id, _pwd):
        self.stu_id = _id
        self.stu_password = _pwd
        self.TIME = int(round(time.time() * 1000))
        self.driver = webdriver.Chrome()

    def login(self):
        driver = self.driver
        url = 'http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html'
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="yhm"]').send_keys(self.stu_id)
        driver.find_element_by_xpath('//*[@id="mm"]').send_keys(self.stu_password)
        code_image = driver.find_element_by_xpath('//*[@id="yzmPic"]')
        path = './image/yzm.png'
        code_image.screenshot(path)
        yzm = generator(path)
        driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(yzm)
        driver.find_element_by_xpath('//*[@id="dl"]').click()

    def cookie(self):
        self.login()
        time.sleep(0.2)
        cookies = self.driver.get_cookies()
        self.driver.quit()
        cookies = cookies[1]['name'] + '=' + cookies[1]['value']  # +'; X-LB='+cookie[0]['value']
        return cookies
