from rob_demo3 import Rob
from moudles.ext import ID, PWD
# 1: '主修课程',
# 2: '跨专业本硕一体化拓展课程组',
# 3: '劳育理论教学',
# 4: '劳育实践教学',
# 5: '板块课(体育)',
# 6: '通识选修课'

kcid = ['Q11035']
# kcid = ['孟献峰']
# kcid = ['P30102']

hdh = Rob(ID, PWD)
hdh.rob(kcid, 1, 4)


