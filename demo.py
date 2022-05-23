# 加载配置
from moudles.ext import ID, PWD


# Login模块使用
from localLogin.Login import FastLogin
# 获得一个登录对象
hdh = FastLogin(ID, PWD)
# 获得cookie
cookies = hdh.get_cookies()
# 获得session
session = hdh.get_session()


# getSth模块使用
from getSth import Stu
# 获得学生对象
hdh = Stu(ID, PWD)
# 获取成绩
# 参数：学年(int) 学期号(int) --> {科目=>[平时分，期末分，总分，学分，绩点]}(dict)
# 全部 空
# 1学期 3
# 2学期 12
# 3学期 16
hdh.getScores(2021)
# 获取课表
# 参数同上
hdh.getCourses(2021)