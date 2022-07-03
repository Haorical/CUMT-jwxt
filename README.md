# 一种应用于中国矿业大学教务系统的数据采集系统

## 免责声明
本代码仅用于学习，下载后请勿用于商业用途。

在使用本项目时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任。

如您在使用本项目的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。 

在使用本工具前，请您务必审慎阅读、充分理解各条款内容，限制、免责条款或者其他涉及您重大权益的条款可能会以加粗、加下划线等形式提示您重点注意。 除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要使用本项目。

您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。 

## 快速开始

建议在虚拟环境下运行，首先安装依赖包

    pip install -r requirements.txt

参考配置部分配置好config.yml后，直接运行main.py即可，全部封装为组件，适合二次开发。

具体方法使用可参考demo.py

## 功能

### 模拟登录接口实现

#### 简介
**模拟登录基于flask,并已经部署到了服务器上，并提供了相应接口供使用，该项目将不再开源，下面只提供实现思路。**

一共写了两个版本，一个是使用selenium的SlowLogin(已废弃)；另一个是基于requests的
FastLogin，秒登，速度飞起，**当然服务器上的只有FastLogin!**

#### 实现
先说SlowLogin，比较无脑，获得输入框的xpath，然后直接sendkeys，这里有个比较麻烦
的就是验证码的问题，这里我用了webdriver的screenshot方法，将图片保存到本地，然后调用
本地的ocr，而且存在识别错现象。因为本来就不是很智能，用人眼看填验证码的话
就更不智能了。

FastLogin这个就非常智能，模拟了发包过程，通过分析登录操作可以知道，先get RSA的公钥再get验证码，分析前端加密js可知，是通过rsa对password进行了加密，我们可以用简单的用python模拟，考虑到搭建环境太复杂，这里是模拟的，没有用exejs和node.js，因此耗费了很长时间，其中jsFunction模拟了js中对RSA的加密。由于get的验证码是二进制文件
我们可以直接将其写入文件中，然后调用本地AI识别，或者人工识别，两个函数在FastLogin中可以自由选择，可以通过config.yml进行设置(服务器端默认AI识别)

```python
# 智能人工识别验证码
code = get_code_by_people(sessions)
# 人工智能识别验证码
code = get_code_by_ocr(sessions)
```
config如下
```
opinions:
  - AI: true
```
调用人工识别函数的时候比较有趣，如下，会弹出窗口，然后人工识别

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916224421.png)

成功获得了cookie

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916224809.png)

ocr识别的话，如下

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916225044.png)

只识别了一次，如果识别错误的话，会自动重新登录，直到登录成功

### 爬取成绩

分析抓包即可，页面逻辑比较简单，post后返回的是json数据，解析，保存成了字典，{科目=>[平时分，期末分，总分，学分，绩点]}，因为获得平时分时需要每一科都请求一次，因此速度比较慢！

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916230422.png)

### 爬取课表

与爬取成绩类似，之后将进行图形化处理。

## 二次开发示例

新成绩微信自动提醒功能实现

```py
    hdh = Stu(ID, PWD)
    sc = {}
    lsc = hdh.getScores(2021,12)
    wcnt = 0
    while 1:
        try:
            nsc = hdh.getScores(2021,12)
            print(nsc)
        except:
            sleep(5)
            pass
        if nsc != lsc:
            sc = nsc
            for cnm in sc:
                if cnm not in lsc:
                    title = cnm + '出成绩了！'
                    data = sc[cnm]
            try:
                if data[4] == '5.00':
                    title += '恭喜你！满绩了！'
                elif data[4] == '4.50':
                    title += '还行！4.5'
                else:
                    title += f'只有{data[4]}哦！'
                mes = f"""
        总分：{data[2]}

        平时分：{data[0]}

        期末分：{data[1]}

        绩点：{data[4]}
                """
            except:
                title='出成绩了'
                mes=str(data)
                pass
            sendMessage(title, mes)
            lsc = nsc
        sleep(30+random.randint(0,30))
        wcnt += 1
        if wcnt == 400:
            sendMessage('运行正常','1111')
            wcnt = 0
```

## 配置
可直接在full_config.yml更改后，重命名为config.yml，id和password为必填项，为教务系统学号和密码

```yaml
api:
  - url: 
  - key: 
  - server: 

user:
  - id: '*********'
  - password: '**********'

opinions:
  - AI: true
```

## 选课模块效果展示

经过多次迭代，目前已具有极强的鲁棒性，几乎实现了绝大部分功能，同时为避免影响正常选课同学选课权益
，demo2/3将不再开源， 已开源的demo1因版本问题早已无法使用。

> 以下图片出现的课程，均为过去本人通过正常手段正常选课所得

### 分类抢课

    1: '主修课程', 
    2: '跨专业本硕一体化拓展课程组', 
    3: '劳育理论教学', 
    4: '劳育实践教学', 
    5: '板块课(体育)', 
    6: '通识选修课'

#### 体育课
![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/202207040116392.png)

#### 公选课
![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/202207040126208.png)

#### 劳动实践
> 因本人过去已选修过该类课程，故没有选课成功的提示，只有过程展示

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/202207040129091.png)

### 条件选课
可按课程号或教师姓名等多种条件选课

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/202207040134988.png)

### 多课程选课
可同时选多门课

    kcid = ['Q30127', 'Q11035']

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/202207040139473.png)

### 多线程选课
基于py threading模块，可自定义抢课线程数量，每秒至少上百次请求，快人一步

    rob(self, kcid: list, thread_num: int, xid: int)


