# 中国矿业大学正方教务爬虫

## 前言

配置好后直接运行main.py就可以体验爬取成绩的功能，代码可读性良好，适合二次开发。

本着服务抗大学子的宗旨，写了这个教务爬虫，用来练手，应该会开发一段时间，目前只
实现了模拟登录和爬取成绩，万众瞩目的自动抢课功能由于当前没有开放选课，暂时无法
开发，暂时搁置。

## 功能

### 模拟登录

#### 简介
一共写了两个版本，一个是使用selenium的SlowLogin，看名字就看出来了，这个登录的慢
而且需要配置webdriver，登录一次大约需要8-10秒钟；另一个是基于requests的
FastLogin，这个顾名思义就相当的快了，登录一次不到五秒钟，速度飞起，而且可能我用的
vpn比较卡，在校园网上应该能更快。

两个版本可以自由切换,在config中设置即可，更改login即可

```python
opinions:
  - login: 'fast'
```

两个模拟登录都可以直接返回成功登录之后的cookie，可以用来爬之后的界面，非常适合二次开发，欢迎二次开发，最好给个star :)

#### 实现
先说SlowLogin，比较无脑，获得输入框的xpath，然后直接sendkeys，这里有个比较麻烦
的就是验证码的问题，这里我用了webdriver的screenshot方法，将图片保存到本地，然后调用
本地的ocr，而且存在识别错现象。因为本来就不是很智能，用人眼看填验证码的话
就更不智能了。

FastLogin这个就非常智能，模拟了发包过程，通过分析登录操作可以知道，先get RSA的公钥再get验证码，分析前端加密js可知，是通过rsa对password进行了加密，我们可以用简单的用python模拟，考虑到搭建环境太复杂，这里是模拟的，没有用exejs和node.js，因此耗费了很长时间，其中jsFunction模拟了js中对RSA的加密。由于get的验证码是二进制文件
我们可以直接将其写入文件中，然后调用本地AI识别，或者人工识别，两个函数在FastLogin中可以自由选择，可以通过config.yml进行设置

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

可以看到成功获得了cookie

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916224809.png)

ocr识别的话，如下

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916225044.png)

可以看到，只识别了一次，如果识别错误的话，会自动重新登录，直到登录成功

### 爬取成绩

分析抓包即可，页面逻辑比较简单，post后返回的是json数据，解析，保存成了字典，{科目=>[平时分，期末分，总分，学分，绩点]}，因为获得平时分时需要每一科都请求一次，因此速度比较慢，其中也有一些选项，自己探索吧，懒得写了，睡觉！

![](https://my-photos-test.oss-cn-hangzhou.aliyuncs.com/2021/20210916230422.png)

一些设置如下，需要保存在config.yml中
```yaml
user:
  - id: 'xxxxxxxx' # 学号
  - password: 'xxxxxxxxxx' # 密码
opinions:
  - AI: true # AI识别验证码选项 true/false
  - login: 'fast' # 登录方式 fast/slow
```